import os
from Libraries.database import Database
import logging

logger = logging.getLogger(__name__)

class Metrics:
    def __init__(self):
        #(os.environ.get("INFLUXDB_URL"), os.environ.get("INFLUXDB_TOKEN"), os.environ.get("INFLUXDB_ORG"), os.environ.get("INFLUXDB_BUCKET"))
        self.dbObj = Database(os.environ.get("INFLUXDB_URL"), os.environ.get("INFLUXDB_TOKEN"), os.environ.get("INFLUXDB_ORG"), os.environ.get("INFLUXDB_BUCKET"))

    def add(self,metricsData, uuid):
        for metric, metricValue in metricsData.items():
            if not metricValue:
                metricValue = "NULL"

            if not isinstance(metricValue,(int, float, str, dict)):
                logger.error(f"Datatype mismatch! {metric} has a value {metricValue} of type ", type(metricValue), " - NOT SUPPORTED!")
                return
            
        try:
            self.dbObj.write(metricsData, uuid)
            logger.info("Called database write method")
        
        except Exception as e:
            logger.error(f"Error occured while calling the database write method: {e}")


    def get(self, timePeriod=None, uuid=None):
        try:
            data = self.dbObj.read(timePeriod, uuid)
            logger.info("Called database read method")

            return data
        
        except Exception as e:
            logger.error(f"Error occured while calling the database read method: {e}")