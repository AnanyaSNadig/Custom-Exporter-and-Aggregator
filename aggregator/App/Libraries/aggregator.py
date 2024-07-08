import requests, os, datetime, json, time, logging, dateutil.parser
from Libraries.registry import Registry
from Libraries.database import Database
from Libraries.metrics import Metrics

logger = logging.getLogger(__name__)

class Aggregator:
    def __init__(self):
        # self.listOfServers = Registry().serverDetails
        regObj = Registry()
        self.listOfServers = regObj.loadRegistry()
        
        # with open('/Users/ananya/Downloads/Hyperface/shellScripts/Internship/ExporterAggregator/Files/aggregatorConfiguration.json', 'r') as file:
        #     config = json.load(file)

        scriptDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(scriptDir)
        filesDir = os.path.join(parentDir, "Files")
        configFilePath = os.path.join(filesDir, "aggregatorConfiguration.json")
        

        with open(configFilePath, 'r') as file:
            config = json.load(file)
            
        self.port = config["port"]
        self.intervalTime = config["intervalTime"]
        self.retryCount = config["retryCount"]


    def collect(self, uuid, data):
        ipAddress = data["ip_addr"]
        # metricsToCollect = data["metrics"]

        getUrl = f"http://{ipAddress}:{self.port}/metrics" 

        # if metricsToCollect:
        #     filters = ",".join(metricsToCollect)
        #     getUrl += f"?filter={filters}"

        try:
            httpResponse = requests.get(getUrl, timeout=5)

            if httpResponse.status_code == 200:
                metricsData = httpResponse.json()
                metricsObj = Metrics()
                metricsObj.add(metricsData, uuid)
                logger.info(f"Successfully sent the GET request to server with uuid {uuid} and received the metrics")

        except Exception as e:
            logger.error(f"GET request to {uuid} server failed with error: {e}")
            self.decideRetry(uuid, data)


    def remove(self, uuid):
        regObj = Registry()

        try:
            regObj.remove(uuid)
            logger.info("Called remove method of registry class")
        
        except Exception as e:
            logger.error(f"Failed to call remove method of registry class with error : {e}")


    def getTimestamp(self, uuid):
        dbObj = Database(os.environ.get("INFLUXDB_URL"), os.environ.get("INFLUXDB_TOKEN"), os.environ.get("INFLUXDB_ORG"), os.environ.get("INFLUXDB_BUCKET"))
        timestamp = dbObj.readLastTimeStamp(uuid)

        if timestamp:
            accessTimestamp = dateutil.parser.parse(timestamp)
            isoFormattedTimestamp = accessTimestamp.isoformat()
            timestampDatetime = datetime.datetime.fromisoformat(isoFormattedTimestamp)
            print("\n FROM THE DB \n")
            return timestampDatetime
        
        else:
            logger.info(f"Either there are no entries of the server with uuid {uuid} or it was polled in the last {self.intervalTime} seconds")
            regObj = Registry()
            # registeredTimestamp = dateutil.parser.parse(regObj.serverDetails[uuid]["timestamp"])
            serverDetails = regObj.loadRegistry()
            registeredTimestamp = dateutil.parser.parse(serverDetails[uuid]["timestamp"])
            print("\n FROM THE REGISTRY \n")
            return registeredTimestamp
           
        
    def decideRetry(self, uuid, data):
        timestamp = self.getTimestamp(uuid)

        if datetime.datetime.now() >= timestamp + datetime.timedelta(seconds=(self.intervalTime * self.retryCount)):
            self.remove(uuid)
            logger.info(f"Called remove method of aggregator class")

        else:  # else part is handled by cron job
            time.sleep(self.intervalTime)
            self.collect(uuid, data)
