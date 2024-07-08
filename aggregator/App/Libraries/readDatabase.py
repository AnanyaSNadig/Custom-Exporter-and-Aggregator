from Libraries.metrics import Metrics
from flask import Flask, request

app = Flask(__name__)

@app.route("/read_db", methods=['GET'])
def readDB():
    time_period = request.args.get('timePeriod', default=None)
    uuid = request.args.get('uuid', default=None)

    metricsObj = Metrics()
    data = metricsObj.get(time_period, uuid)
    dataDict = {}

    if data:
        dataDict = data

    return dataDict


if __name__ == "__main__":
    app.run(debug=True, port=5003)
