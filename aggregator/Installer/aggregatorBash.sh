#!/bin/bash

SCRIPT_DIR="$(pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

REQUIREMENTS_PATH="$SCRIPT_DIR/requirements.txt"
GUNICORN_WSGIDB_FILE="wsgiDB"
GUNICORN_WSGIPOST_FILE="wsgiPOST"
GUNICORN_APP="app"
GUNICORN_BIND_ADDRESS_DB="0.0.0.0:5003"
GUNICORN_BIND_ADDRESS_POST="0.0.0.0:9101"
AGGREGATOR_SCRIPT="$PARENT_DIR/App/aggregatorMain.py"
LOG_DIR="$PARENT_DIR/App/Files"

echo $LOG_DIR

# INFLUX DB
INFLUXDB_TOKEN="2g3qrtQJXYv8HzZ2LSDIlliD-Ev5L-cHEmCycDf9R2SxnDkQjdHEoDvMgsdakGcUxio0EfUNdl9LAJW55v2AWQ=="
INFLUXDB_ORG="infra"
INFLUXDB_URL="http://localhost:8086"
INFLUXDB_BUCKET="pulledMetrics"

# sudo apt-get update && sudo apt-get install -y python3-pip
# brew upgrade && brew install python3 && brew install pip

VENV_DIR="$PARENT_DIR/venv"
python3 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

echo "Installing required Python packages"
pip3 install -r $REQUIREMENTS_PATH

cd $PARENT_DIR/App
echo "Starting Gunicorn servers"
echo "Gunicorn: $(which gunicorn)"
$(which gunicorn) --workers 4 --bind $GUNICORN_BIND_ADDRESS_POST --log-level=info --daemon $GUNICORN_WSGIPOST_FILE:$GUNICORN_APP > $LOG_DIR/gunicorn_POST.log 2>&1
$(which gunicorn) --workers 4 --bind $GUNICORN_BIND_ADDRESS_DB --log-level=info --daemon $GUNICORN_WSGIDB_FILE:$GUNICORN_APP > $LOG_DIR/gunicorn_DB.log 2>&1

echo "Scheduling aggregator script as a cron job to poll metrics"
cd $VENV_DIR
(crontab -l 2>/dev/null; echo "* * * * * INFLUXDB_TOKEN='$INFLUXDB_TOKEN' INFLUXDB_ORG='$INFLUXDB_ORG' INFLUXDB_URL='$INFLUXDB_URL' INFLUXDB_BUCKET='$INFLUXDB_BUCKET' $(which python3) $AGGREGATOR_SCRIPT >> $VENV_DIR/aggregator_cron_new.log 2>&1") | crontab -

echo "Custom Aggregator setup completed successfully."
