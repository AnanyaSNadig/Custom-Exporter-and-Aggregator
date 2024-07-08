import logging, os

scriptDir = os.path.dirname(os.path.abspath(__file__))
filesDir = os.path.join(scriptDir, "Files")
logFilePath = os.path.join(filesDir, "logs.log")

logging.basicConfig(filename=logFilePath, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from Libraries.aggregator import Aggregator
from Libraries.database import Database
from Libraries.metrics import Metrics
from Libraries.registry import Registry
import Libraries.getPostRequestData

# logging.Formatter.converter = time.gmtime

class Main:
    def runAggregator(self):
        logger.info(f"About to start collecting metrics ...")
        aggObj = Aggregator()
        print("\nSTARTING AGGREGATOR NOW\n")
        print(aggObj.listOfServers)
        for uuid, serverData in aggObj.listOfServers.items():
            print("Found a server entry")
            print(f"uuid = {uuid}, data = {serverData}")
            aggObj.collect(uuid, serverData)


def main():
    mainObj = Main()
    print("Running the aggregator")
    mainObj.runAggregator()
    

if __name__ == "__main__":
    main()

