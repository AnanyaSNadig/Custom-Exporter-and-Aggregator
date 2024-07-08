# Custom-Exporter-and-Aggregator

## Overview

This project comprises a custom aggregator and custom exporter system designed to collect and export metrics from multiple sources. The aggregator pulls metrics from all registered exporters, while each exporter posts its available metrics to the aggregator. This system ensures continuous monitoring and re-registration of exporters if they go down and come back up.



## Components

### Aggregator

The aggregator component maintains a registry of exporters and periodically pulls metrics from them. It uses a Gunicorn server for handling requests and InfluxDB for storing metrics.

#### Directory Structure:

* Installer/: Contains a bash script (aggregatorBash.sh) for one-step installation, setting up the necessary packages from requirements.txt, and configuring a cron job to pull metrics periodically.
  
* App/:
  - Libraries/: Contains Python files for database operations, registry updates, handling POST requests, and metric collection via API calls.
  
  - Files/: Includes configuration files (config.json for pull intervals, retries, and API ports, server_registry.json for storing exporter details) and log files for Gunicorn and aggregator.
  
  - aggregatorMain.py: The main script executed by the cron job to pull metrics.
  
  - wsgiDB.py: Runs the Gunicorn server for the InfluxDB Flask app.
  
  - wsgiPOST.py: Runs the Gunicorn server to handle POST request data.


### Exporter
Each exporter component is responsible for sending its metrics to the aggregator. It uses a common directory structure for all exporters, with one-step installation via a bash script.

#### Directory Structure:

* config.json: Configuration file containing settings such as aggregator URL.
  
* common.json: File for storing UUID and posting time.
  
* metric_exporter.py: Exposes system metrics. New metrics should be added here and updated in the metric_api.py collector method.
  
* metric_api.py: Responds to aggregator GET requests by sending system metrics using methods from metric_exporter.py.
  
* ip_fetcher.py: Fetches the system IP and updates config.json.
  
* post_request.py: Responsible for posting UUID, IP, and time to the aggregator. Utilizes config.json for aggregator URL/IP and writes UUID and recent time to common.json.
  
* log_file.log: Log file for recording post_request.py activities.
  
* installation.sh: Shell script for installation.
  
* requirements.txt: File containing dependencies required for the exporter.



## Installation and Setup

### Clone the Repository

```console
git clone <repository url>
```

### Setting Up the Aggregator

#### Step 1: Install InfluxDB
For Linux:
```console
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.9-linux-amd64.tar.gz
tar xvzf influxdb2-2.0.9-linux-amd64.tar.gz
sudo cp influxdb2-2.0.9-linux-amd64/influx /usr/local/bin/
```

For macOS:
```console
brew install influxdb
```

For Windows:

Download from the official site and extract the executable to a desired location.


#### Step 2: Start InfluxDB Service
For Linux:
```console
sudo systemctl start influxdb
```

For macOS using Homebrew:
```console
brew services start influxdb
```

For Windows:

Run the influxd.exe executable directly from the command line.


#### Step 3: Initial Setup via Web Interface

Open your web browser and go to http://localhost:8086.

Complete the initial setup:

* Enter your username.
  
* Enter your password.
  
* Enter your organization name.
  
* Enter your bucket name.
  
* Click Continue to complete the setup.


#### Step 4: Generate a Token via Web Interface

* Log in to the InfluxDB web interface.
  
* Navigate to the Tokens section:
  
  - Click on the Data tab on the left-hand sidebar.
  
  - Click on Tokens.

* Create a new token:
  
  - Click on the Generate Token button.
  
  - Choose the type of token you need (e.g., All Access Token, Read/Write Token).
  
* Copy the generated token from the web interface.

  
#### Step 5: Run the Aggregator Installer

Navigate to the Installer directory in the aggregator directory and execute the following with sudo permissions:
```console
sudo chmod +x aggregatorBash.sh
sudo ./aggregatorBash.sh
```


### Setting Up the Exporter

Run the following commands under sudo permissions and ensure the working directory is the exporter file:
```console
sudo chmod +x installation.sh
sudo ./installation.sh
```



### Daemon Service Verification

After installation of the exporter, verify that a daemon service is added to the system by executing the following commands:
```console
cd /etc/systemd/system
systemctl status metrics_api_final.service
```

The output should confirm the service status.



### Cronjob Verification
Verify that the cronjob is added by running the following command:
```console
sudo crontab -l -u root
```

The output should display the cronjob configuration.



## Usage

Once the aggregator and exporters are set up and running, the system will automatically manage the registration and periodic pulling of metrics. The InfluxDB instance will store the collected metrics, which can be accessed and analyzed as needed.

For further customization and configuration, refer to the respective config.json, common.json, and logging files within the aggregator and exporter directories.