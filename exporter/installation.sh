#!/bin/bash

# Determine the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
APP_FILE="metric_api:app"  
SERVICE_FILE="/etc/systemd/system/metric_api.service"
USERNAME="$(whoami)"  # Replace 'your_username' with the appropriate username
NUM_WORKERS="4"
BIND_ADDRESS="0.0.0.0:8081"
REQUIREMENTS_PATH="$SCRIPT_DIR/requirements.txt"  # Adjust this path accordingly

# Update package repositories and install necessary packages
sudo apt-get update && sudo apt-get install -y python3-pip
pip3 install -r "$REQUIREMENTS_PATH"
pip3 install gunicorn

# Find the path to the gunicorn executable
GUNICORN_PATH=$(which gunicorn)

# Function to update IP address in configuration file using the python script
update_ip_in_config() {
    $(which python3) "$SCRIPT_DIR/configurations/ip_fetcher.py"
}

# Create the service file
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Metric API service
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$SCRIPT_DIR/metrics_api_modules/
Environment="FLASK_APP=metric_api.py"
ExecStart=$GUNICORN_PATH -w $NUM_WORKERS -b $BIND_ADDRESS $APP_FILE
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon to apply changes
sudo systemctl daemon-reload

# Start the service
sudo systemctl start metric_api

# Enable the service to start on boot
sudo systemctl enable metric_api

# Check the status of the service
sudo systemctl status metric_api

# Add a cron job to execute post_request.py
(crontab -l 2>/dev/null; echo "* * * * * cd $SCRIPT_DIR/registrations/ && /usr/bin/python3 post_request.py >> $SCRIPT_DIR/registrations/log_file.log 2>&1") | crontab -
