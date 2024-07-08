from influxdb_client import InfluxDBClient
from influxdb import line_protocol
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, url, token, org, bucket):
        # Sets up the client with the provided connection details and stores the bucket and organization information.

        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket
        self.org = org


    def read(self, timePeriod=None, uuid=None):
        # Queries the database for data. 
        # It can filter data based on time period and UUID. 
        # The method constructs a Flux query, executes it, and formats the results into a list of dictionaries containing relevant data fields.

        queryAPI = self.client.query_api()

        query = f'from (bucket: "{self.bucket}")'

        if timePeriod is not None:
            query += f' |> range(start: -{timePeriod}m)'

        else:
            query += f' |> range(start: -24h)'


        if uuid is not None:
            query += f' |> filter(fn: (r) => r.host == "{uuid}")'

        try:
            queryData = queryAPI.query(org=self.org, query=query)

            results = []
            for table in queryData:
                for record in table.records:
                    data = {
                        # "time": record.get_time(),
                        "uuid" : record.values.get("host"),
                        "access_time" : record.values.get("lastAccessTimestamp"),
                        "measurement": record.get_measurement(),
                        "field": record.get_field(),
                        "value": record.get_value()
                    }
                   
                    results.append(data)
            
            return results
        
        except Exception as e:
            logger.error(f"An error occurred while reading the database: {e}")
       

    def write(self, metricsData, uuid):
        # Accepts metrics data and a UUID to write data points to the database. It formats the data into line protocol format and uses the synchronous write API to write the data to InfluxDB.

        pointsValue = []

        lastAccessedTimestamp = metricsData.pop("timestamp")

        for metric, metricValue in metricsData.items():
            # print(f" Metric: {metric} , Value {metricValue}")
            if metricValue is None:
                metricValue = "NULL"

            if isinstance(metricValue, dict):  
                fields = metricValue

                for key, value in fields.items():
                    if value is None:
                        value = "NULL"

            else:
                fields = {"value": metricValue}

            point = {
                "measurement" : metric,
                "tags" : {"host" : uuid, "lastAccessTimestamp" : lastAccessedTimestamp},
                "fields" : fields
            }
            pointsValue.append(point)

        jsonData = {"points" : pointsValue}
        lineProtocolData = line_protocol.make_lines(jsonData)

        try:
            writeAPI = self.client.write_api(write_options=SYNCHRONOUS)
            writeAPI.write(bucket=self.bucket, org=self.org, record=lineProtocolData)
            logger.info(f"Data recieved from the server {uuid} was successfully written into InfluxDB")

        except Exception as e:
            logger.error(f"Error writing data to InfluxDB: {e}")
            

    def readLastTimeStamp(self,uuid):
        
        print("Inside readLastTimestamp\n")
        queryAPI = self.client.query_api()

        query = f'from(bucket:"{self.bucket}") |> range(start: -24h) |> filter(fn: (r) => r["host"] == "{uuid}") |> group() |>last()'

        try:
            result = queryAPI.query(org=self.org, query=query)

            for table in result:
                for record in table.records:
                    column_value = record.values.get("lastAccessTimestamp")
                    logger.info(f"The value of timestamp for the server with UUID {uuid} is retrieved successfully: {column_value}")
                    return column_value
                
        except Exception as e:
            logger.error(f"Failed to read the value of timestamp, error: {e}")