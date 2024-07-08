from flask import Flask, jsonify, request  # Importing Flask and related modules
import psutil  # Importing psutil for system metrics
from abc import ABC, abstractmethod  # Importing ABC and abstractmethod for defining abstract classes
from datetime import datetime  # Importing datetime for timestamp


class MetricCollector(ABC):
    @abstractmethod
    def collect(self):
        pass  # Abstract method to be implemented by subclasses


class MetricContext:
    def __init__(self, collector):
        self.collector = collector  # Initializing with a metric collector instance

    def collect(self):
        return self.collector.collect()  # Delegating collection to the associated collector


class CPUMetricCollector(MetricCollector):
    def collect(self):
        return psutil.cpu_percent(interval=1)  # Collecting CPU usage percentage


class RAMMetricCollector(MetricCollector):
    def collect(self):
        return psutil.virtual_memory().percent  # Collecting RAM usage percentage


class DiskMetricCollector(MetricCollector):
    def collect(self):
        return psutil.disk_usage('/').percent  # Collecting disk usage percentage


class ThroughputMetricCollector(MetricCollector):
    def __init__(self):
        self.last_io_counters = psutil.net_io_counters()  # Initializing with the last network I/O counters

    def collect(self):
        current_io_counters = psutil.net_io_counters()  # Getting current network I/O counters
        # Calculating bytes sent and received since the last measurement
        bytes_sent = current_io_counters.bytes_sent - self.last_io_counters.bytes_sent
        bytes_recv = current_io_counters.bytes_recv - self.last_io_counters.bytes_recv
        self.last_io_counters = current_io_counters  # Updating last counters for the next measurement
        return {'bytes_sent': bytes_sent, 'bytes_recv': bytes_recv}  # Returning network throughput metrics


class TimestampMetricCollector(MetricCollector):
    def collect(self):
        timestamp = datetime.now().isoformat(timespec='microseconds') + 'Z'  # Generating ISO-formatted timestamp
        return timestamp  # Returning timestamp
