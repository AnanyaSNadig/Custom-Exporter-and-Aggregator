import json, os, datetime
import logging

logger = logging.getLogger(__name__)

class Registry:
    def __init__(self):
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(scriptDir)
        filesDir = os.path.join(parentDir, "Files")
        filePath = os.path.join(filesDir, "serverRegistry.json")
        self.filePath = filePath

    def loadRegistry(self):
        if os.path.exists(self.filePath) and os.path.getsize(self.filePath) > 0:
            with open(self.filePath, 'r') as file:
                serverDetails = json.loads(file.read())
        
        else:
            serverDetails = {}

        return serverDetails
    

    def writeToJSONfile(self, serverDetails):
        with open(self.filePath, 'w') as file:
            json.dump(serverDetails, file)


    def add(self, listOfDetails):
        latestServerRegDetails = self.loadRegistry()

        uuid = listOfDetails["uuid"]
        ipAddress = listOfDetails["ip_addr"]
        # metricsToMonitor = listOfDetails["metrics"]
        registeredTimestamp = str(listOfDetails["timestamp"])

        if uuid not in latestServerRegDetails.keys():
            serverEntry = {uuid: {"ip_addr" : ipAddress, "timestamp" : registeredTimestamp}}
            latestServerRegDetails.update(serverEntry)
            self.writeToJSONfile(latestServerRegDetails)
            print(f"\n{latestServerRegDetails} - after adding\n")

            logger.info(f"Successfully added details of server {uuid} to the server registry")

        else:
            logger.info(f"Server with uuid {uuid} is already registered")
        

    def remove(self, uuid):
        serverDetails = self.loadRegistry()
        if len(serverDetails) == 0:
            logger.info("The server registry is empty")
           
        else:
            if uuid in serverDetails:
                del serverDetails[uuid]
                self.writeToJSONfile(serverDetails)
                logger.info(f"Deleted the entry of server with uuid {uuid} from the server registry")
            else:
                logger.info(f"The server with uuid {uuid} is not registered")