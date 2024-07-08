Custom Exporter Installation Manual

Introduction:
The exporter is responsible for exposing system metrics and responding to pull requests from the aggregator. This manual outlines the steps required to set up the exporter on the host/server system.

Installation Steps:
Step 1: Environment Setup
Download the exporter files and navigate to the exporter directory. Ensure the following files are present:
config.json: Configuration file containing settings such as aggregator URL.
common.json: File for storing UUID and posting time.
metric_exporter.py: Exposes system metrics. New metrics should be added here and updated in the `metric_pi.py` collector method.
metric_api.py: Responds to aggregator GET requests by sending system metrics using methods from `metric_exporter.py`.
ip_fetcher.py: Fetches the system IP and updates `config.json`.
post_request.py: Responsible for posting UUID, IP, and time to the aggregator. Utilises `config.json` for aggregator URL/IP and writes UUID and recent time to `common.json`.
log_file.log: Log file for recording post_requset.py activities.
installation.sh: Shell script for installation.
requirements.txt: File containing dependencies required for the exporter.

Step 2: Installation
Run the following commands under sudo permissions and ensure the working directory is the exporter file:
sudo chmod +x installation.sh
sudo ./installation.sh


Step 3: Daemon Service Verification
After installation, verify that a daemon service is added to the system by executing the following commands:
cd /etc/systemd/system
systemctl status metrics_api_final.service

The output should confirm the service status.

Step 4: Cronjob Verification
Verify that the cronjob is added by running the following command:
sudo crontab -l -u root


The output should display the cronjob configuration.

This completes the installation. The exporter, if installed properly, should be up and running with the aforementioned configurations.


