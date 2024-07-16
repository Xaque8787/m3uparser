from jellyfin_apiclient_python import JellyfinClient
from parser.jellyfin_api.utility.server_init import jellyfin_url, api_key

def run_guide_task():
    # Use built-in method to get default headers
    apikey_ezpztv = JellyfinClient()
    apikey_ezpztv.config.app('EZPZTV', '21.12', 'device', '123456')
    apikey_ezpztv.config.data["auth.ssl"] = True
    apikey_ezpztv.authenticate(
        {"Servers": [
            {"AccessToken": api_key, "address": jellyfin_url}]}, discover=False)

    headers = apikey_ezpztv.jellyfin.get_default_headers()

    try:
        # Send POST request to the specified endpoint
        response = apikey_ezpztv.jellyfin.send_request(
            jellyfin_url,
            "ScheduledTasks/Running/bea9b218c97bbf98c5dc1303bdb9a0ca",
            method="post",
            headers=headers
        )

        if response.status_code == 204:
            print("Scheduled task started successfully.")
        else:
            print(f"Failed to start scheduled task. Status Code: {response.status_code}, Response: {response.content}")

    except Exception as e:
        print(f"Failed to start scheduled task: {e}")


def run_library_task():
    # Use built-in method to get default headers
    apikey_ezpztv = JellyfinClient()
    apikey_ezpztv.config.app('EZPZTV', '21.12', 'device', '123456')
    apikey_ezpztv.config.data["auth.ssl"] = True
    apikey_ezpztv.authenticate(
        {"Servers": [
            {"AccessToken": api_key, "address": jellyfin_url}]}, discover=False)

    headers = apikey_ezpztv.jellyfin.get_default_headers()

    try:
        # Send POST request to the specified endpoint
        response = apikey_ezpztv.jellyfin.send_request(
            jellyfin_url,
            "/Library/Refresh",
            method="post",
            headers=headers
        )

        if response.status_code == 204:
            print("Library refresh task started successfully.")
        else:
            print(f"Failed to start Library refresh task. Status Code: {response.status_code}, Response: {response.content}")

    except Exception as e:
        print(f"Failed to start Library refresh task: {e}")

# if __name__ == "__main__":
#     run_guide_task()
#     run_library_task()