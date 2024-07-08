from flask import Flask, request
from Libraries.registry import Registry
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

regObj = Registry()

@app.route('/api/post',methods=['POST'])
def retrievePOSTdata():
    data = request.json
    regObj.add(data)
    logger.info("Recieved server details from an exporter")

    return data
    
if __name__ == "__main__":
    app.run(debug=True)
