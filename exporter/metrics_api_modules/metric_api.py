from flask import Flask, jsonify
from metric_exporter import *  # Importing metric exporter module

class MetricsAPI:
    def __init__(self):
        self.app = Flask(__name__)  # Initializing Flask app
        self.register_routes()  # Registering API routes

    def register_routes(self):
        # Adding a route for fetching metrics
        self.app.add_url_rule('/metrics', methods=['GET'], view_func=self.get_metrics)

    def get_metrics(self):
        all_metrics_data = {}  # Dictionary to hold all metrics data
        collectors = self.get_all_collectors()  # Fetching all metric collectors

        # Iterating through each metric type and collecting data
        for metric_type, collector in collectors.items():
            context = MetricContext(collector)  # Creating metric context
            all_metrics_data[metric_type] = context.collect()  # Collecting data for each metric type

        # Creating a JSON response from collected metrics data
        return self.create_response(all_metrics_data)

    def create_response(self, data):
        # Creating a JSON response with collected metrics data
        if data:
            return jsonify(data), 200  # Returning collected metrics with 200 status code
        else:
            return jsonify({"error": "No metrics found"}), 404  # Returning error message with 404 status code

    def get_all_collectors(self):
        # Defining all available metric collectors
        collectors = {
            'cpu': CPUMetricCollector(),
            'ram': RAMMetricCollector(),
            'disk': DiskMetricCollector(),
            'throughput': ThroughputMetricCollector(),
            'timestamp': TimestampMetricCollector()
        }
        return collectors  # Returning all metric collectors

metrics_api = MetricsAPI()  # Creating instance of MetricsAPI
app = metrics_api.app  # Assigning Flask app to 'app' variable

if __name__ == "__main__":
    # Running the Flask app on specified host and port
    app.run(host='0.0.0.0', port=8080)
