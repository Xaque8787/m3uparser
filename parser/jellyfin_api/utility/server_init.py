import requests
import time
import json
import os
import shutil
import re

# ================================
# Initial Server Configuration
# ================================

# Step 1: Initial server configuration
def configure_server(jellyfin_url, setup_user, setup_pass):

    # Initial configuration
    resp = requests.post(f'{jellyfin_url}/Startup/Configuration',
                         json={"UICulture": "en-US", "MetadataCountryCode": "US", "PreferredMetadataLanguage": "en"})
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

# ================================
# Rename server
# ================================


def rebrand_server(main_client, jellyfin_url, server_name):
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


# ================================
# Ping server
# ================================


def ping_server(jellyfin_url, max_retries=10, interval=10):
    
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(
                jellyfin_url,
                "System/Ping"
            )

            if response.status_code == 200:
                print("PING was successful.")
                try_serv = requests.get(
                    jellyfin_url,
                    "System/Info/Public"
                )
                if try_serv.status_code == 200:
                    print("Server available.")
                    date_header = try_serv.headers.get('Date')
                    if date_header:
                        print(f"Date: {date_header}")
                    else:
                        print("Date header not found.")
                time.sleep(7)
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


# ================================
# Add repository to server
# ================================


def add_repo(main_client, jellyfin_url):

    try:
        headers = main_client.jellyfin.get_default_headers()
        headers.update({
            "Content-Type": "application/json"
        })
        addrepo = [{
                    "Name": "Jellyfin Official Repository",
                    "Url": "https://repo.jellyfin.org/files/plugin/manifest.json",
                    "Enabled": True
        }]

        # Send POST request to the specified endpoint
        response = main_client.jellyfin.send_request(
            jellyfin_url,
            "/Repositories",
            method="post",
            headers=headers,
            data=json.dumps(addrepo)
        )

        if response.status_code == 204:
            print("Repository added successfully.")
        else:
            print(f"Failed to add repository. Status Code: {response.status_code},"
                  f" Response: {response.content}")

    except Exception as e:
        print(f"Failed to add repository: {e}")



# ================================
# Rebrand image
# ================================


def copy_png_files(filename, source_dir, destination_dir):
    # Construct full file paths
    source_path = os.path.join(source_dir, filename)
    destination_path = os.path.join(destination_dir, filename)

    # Check if the source file exists
    if os.path.exists(source_path) and source_path.endswith(('.png', '.ico', '.json')):
        try:
            # noinspection PyTypeChecker
            shutil.copy2(source_path, destination_path)
            print(f"File {filename} copied successfully to {destination_dir}.")
        except Exception as e:
            print(f"Error copying file {filename}: {e}")
    else:
        print(f"File {filename} not found or is not a PNG file in {source_dir}.")


def copy_threadfin_files(filename, source_dir, destination_dir, application_version):
    if application_version == "threadfin":
        try:
            # Construct full file paths
            source_path = os.path.join(source_dir, filename)
            destination_path = os.path.join(destination_dir, filename)

            # Check if the source file exists
            if os.path.exists(source_path) and source_path.endswith(('.png', '.ico', '.json')):
                try:
                    # noinspection PyTypeChecker
                    shutil.copy2(source_path, destination_path)
                    print(f"File {filename} copied successfully to {destination_dir}.")
                except Exception as e:
                    print(f"Error copying file {filename}: {e}")
            else:
                print(f"File {filename} not found or is not a PNG file in {source_dir}.")
        except Exception as e:
            print(f"Error copying file {filename}: {e}")
    else:
        print(f"Application Version is not Threadfin, skipping adding menu item")
# ================================
# Rebrand web title
# ================================


def rebrand_title(logo_file):
    try:
        # Define file paths
        file1 = f'{logo_file}/main.jellyfin.bundle.js'
        file2 = f'{logo_file}/index.html'
        file3 = f'{logo_file}/73233.d08d0c3a593dcbf1c7c7.chunk.js'

        # Define replacements
        replacements = [
            (file1, [
                (r'document\.title=s\.Ay\.translateHtml\(document\.title,"core"\)', 'document.title="EZPZTV"')
            ]),
            (file2, [
                (r'<title>Jellyfin</title>', '<title>EZPZTV</title>')
            ]),
            (file3, [
                (r'document\.title="Jellyfin"', 'document.title="EZPZTV"'),
                (r'document\.title=e\|\|"Jellyfin"', 'document.title=e||"EZPZTV"')
            ])
        ]

        for file_path, file_replacements in replacements:
            try:
                with open(file_path, 'r+', encoding='utf-8') as f:
                    content = f.read()
                    for pattern, replacement in file_replacements:
                        content = re.sub(pattern, replacement, content)
                    f.seek(0)
                    f.write(content)
                    f.truncate()
                print(f"File '{file_path}' was edited successfully.")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    except Exception as e:
        print(f"Error rebranding titles: {e}")
# if __name__ == "__main__":
