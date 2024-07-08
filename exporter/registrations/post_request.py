import logging, uuid, json, requests, os
from datetime import datetime, timedelta

# Get the current working directory and set up the log file path
current_working_dir = os.getcwd()
log_file_path = os.path.join(current_working_dir, 'log_file.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Class for managing JSON files
class JsonFileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    # Read JSON data from the file
    def read_json(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.warning(f"File not found: {self.file_path}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in file {self.file_path}: {e}")
            return None

    # Write JSON data to the file
    def write_json(self, data):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            logging.error(f"Error writing JSON to file {self.file_path}: {e}")

# Class for posting UUID and IP address to an aggregator
class UuidIpPoster:
    def __init__(self, aggregator_url):
        self.aggregator_url = aggregator_url

    # Post UUID and IP address to the aggregator
    def post_uuid_ip(self, uuid, ip_address):
        timestamp = datetime.now()
        data = {'uuid': str(uuid), 'ip_addr': ip_address, 'timestamp': str(timestamp)}
        try:
            response = requests.post(self.aggregator_url, json=data)
            if response.status_code == 200:
                logging.info("UUID and IP posted successfully to the aggregator.")
            else:
                logging.error(f"Failed to post UUID and IP. Status code: {response.status_code}")
        except Exception as e:
            logging.error("An error occurred while posting UUID and IP:", e)

# Class for managing UUIDs
class Uuid:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_manager = JsonFileManager(file_path)

    # Execute the UUID management process
    def execute(self):
        data = self.file_manager.read_json()
        if data is None or not data:
            generated_uuid = str(uuid.uuid4())
            self.file_manager.write_json({"uuid": generated_uuid})
            return generated_uuid
        else:
            return data.get("uuid")

# Class for recording last access time
class LastAccess:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_manager = JsonFileManager(file_path)

    # Record the current access time
    def record_access_time(self):
        data = self.file_manager.read_json() or {}
        data['last_access_time'] = datetime.now().isoformat()
        self.file_manager.write_json(data)

# Class for posting UUID and IP address with timeout check
class UuidIpPosterTimed:
    def __init__(self, common_file_path, aggregator_url, timeout_minutes, ip_address):
        self.common_file_path = common_file_path
        self.aggregator_url = aggregator_url
        self.timeout_minutes = timeout_minutes
        self.ip_address = ip_address
        self.file_manager = JsonFileManager(common_file_path)
        self.uuid_ip_poster = UuidIpPoster(aggregator_url)

    # Post UUID and IP if timeout is reached
    def post_if_timeout_reached(self):
        data = self.file_manager.read_json()
        if not data:
            logging.warning("Common JSON file not found.")
            return

        last_access_time_str = data.get("last_access_time")
        uuid = data.get("uuid")

        if not last_access_time_str:
            logging.warning("Last access time not found in the common JSON file.")
            return

        last_access_time = datetime.fromisoformat(last_access_time_str)
        time_difference = datetime.now() - last_access_time

        if time_difference >= timedelta(minutes=self.timeout_minutes):
            logging.info("Timeout reached. Posting UUID and IP address to the aggregator...")
            self.uuid_ip_poster.post_uuid_ip(uuid, self.ip_address)
        else:
            logging.info("Timeout not reached. No action needed.")


if __name__ == "__main__":
    # Set up file paths and configuration
    common_file_path = os.path.join(current_working_dir, 'common.json')
    config_file_path = os.path.join(current_working_dir, 'config.json')
    config = JsonFileManager(config_file_path)
    # Load JSON configuration
    aggregator_url = config.read_json()['aggregator_url']
    timeout_minutes = config.read_json()['timeout_minutes']
    ip_address = config.read_json()['ip_address']
    # Create and run the timed UUID and IP poster
    uuid_ip_poster_timed = UuidIpPosterTimed(common_file_path, aggregator_url, timeout_minutes, ip_address)
    uuid_ip_poster_timed.post_if_timeout_reached()

    # Manage UUID
    uuid_manager = Uuid(common_file_path)
    uuid_value = uuid_manager.execute()
    logging.info(f"UUID retrieved or generated: {uuid_value}")

    # Record last access time
    last_access_manager = LastAccess(common_file_path)
    last_access_manager.record_access_time()
    logging.info("Last access time recorded.")

    # Post UUID and IP
    uuid_ip_poster = UuidIpPoster(aggregator_url)
    uuid_ip_poster.post_uuid_ip(uuid_value, ip_address)
