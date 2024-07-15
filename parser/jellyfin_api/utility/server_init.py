import requests
import time
import json
from parser.config.variables import *
#================================
# Load env variables
#================================


serv_var = initialize_vars(process_env_variable, str_to_bool, process_env_special)
jellyfin_url = 'http://10.69.7.216:8096'
setup_user = 'jellyfin'
setup_pass = 'jellyfin'
main_user = 'main_user'
main_pass = 'main_pass'
live_tv = serv_var['live_tv']
server_name = serv_var['server_name']
log_file_path = f'{serv_var['logs']}/log_file.log'
epg_path = serv_var['epg_path']
if epg_path:
    epg_path = epg_path.strip('"\'')  # Strip both double and single quotes
else:
    epg_path = ''
#================================
# Initial Server Configuration
#================================

# Step 1: Initial server configuration
def configure_server():

    # Initial configuration
    resp = requests.post(f'{jellyfin_url}/Startup/Configuration', json={"UICulture": "en-US", "MetadataCountryCode": "US", "PreferredMetadataLanguage": "en"})
    assert resp.ok  # Ensure the request was successful
    time.sleep(1)

    # Get startup user configuration
    resp = requests.get(f'{jellyfin_url}/Startup/User')
    assert resp.ok
    time.sleep(1)

    # Create initial user
    resp = requests.post(f'{jellyfin_url}/Startup/User', json={"Name": setup_user, "Password": setup_pass})
    assert resp.ok
    time.sleep(1)

    # Re-apply initial configuration
    payload = {"UICulture": "en-US", "MetadataCountryCode": "US", "PreferredMetadataLanguage": "en"}
    resp = requests.post(f'{jellyfin_url}/Startup/Configuration', json=payload)
    assert resp.ok
    time.sleep(1)

    # Configure remote access
    payload = {"EnableRemoteAccess": True, "EnableAutomaticPortMapping": False}
    resp = requests.post(f'{jellyfin_url}/Startup/RemoteAccess', json=payload)
    assert resp.ok
    time.sleep(1)

    # Complete the startup configuration
    resp = requests.post(f'{jellyfin_url}/Startup/Complete')
    assert resp.ok
    time.sleep(1)

#================================
# Rename server
#================================

def rebrand_server(main_client):
    server_rebrand = {
        "ServerName": server_name,
        "IsStartupWizardCompleted": True
    }

    headers = main_client.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "application/json"
    })

    try:
        response = main_client.jellyfin.send_request(
            jellyfin_url,
            "/System/Configuration",
            method="post",
            headers=headers,
            data=json.dumps(server_rebrand)
        )

        if response.status_code == 204:
            print("Renamed server successfully.")
        else:
            print(f"Failed to rename server. Status Code: {response.status_code}, Response: {response.content}")
    except Exception as e:
        print(f"Failed to rename server: {e}")


#================================
# Ping server
#================================


def ping_server(max_retries=10, interval=10):
    
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(
                jellyfin_url,
                "System/Ping"
            )

            if response.status_code == 200:
                print("PING was successful.")
                return "continue"

            else:
                print(f"Failed to Ping server, Response: {response.content}")
        except Exception as e:
            print(f"Failed to ping server: {e}")

        retry_count += 1
        print(f"Retrying... ({retry_count}/{max_retries})")
        time.sleep(interval)

    print(f"Failed to ping server after {max_retries} retries.")
    return "stop"
