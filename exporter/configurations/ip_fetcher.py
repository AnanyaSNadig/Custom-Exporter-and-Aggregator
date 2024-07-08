import socket
import json

# Function to update the IP address in the configuration file
def update_ip_in_config(ip_address, config_file='registrations/config.json'):
    try:
        # Read the current configuration data from the file
        with open(config_file, 'r') as file:
            config_data = json.load(file)
        # Update the IP address in the configuration data
        config_data['ip_address'] = ip_address
        # Write the updated configuration data back to the file
        with open(config_file, 'w') as file:
            json.dump(config_data, file)
    except Exception as e:
        print("Error:", e)

# Function to retrieve the IP address of the current machine
def get_ip_address():
    try:
        # Create a UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect the socket to a remote address (Google's public DNS server)
        s.connect(('8.8.8.8', 80))
        # Get the local IP address associated with the socket
        ip_address = s.getsockname()[0]
        s.close()  # Close the socket
        return ip_address  # Return the retrieved IP address
    except Exception as e:
        print("Error:", e)
        return None

# Main function
if __name__ == "__main__":
    # Get the current IP address
    ip_address = get_ip_address()
    if ip_address:
        # Update the IP address in the configuration file if retrieved successfully
        update_ip_in_config(ip_address)        
    else:
        print("Failed to retrieve IP address.")
