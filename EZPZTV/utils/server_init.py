import requests
import time
import os
import json


#================================
# Load env variables
#================================

jellyfin_url = 'http://10.21.12.8:8096'
setup_user = 'jellyfin'
setup_pass = 'jellyfin'
main_user = os.getenv('USER_NAME')
main_pass = os.getenv('PASSWORD')
live_tv = os.getenv('LIVE_TV')
server_name = os.getenv('SERVER_NAME')
log_file_path = '/usr/src/app/logs/log_file.log'
epg_path = os.getenv('EPG_URL')
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



