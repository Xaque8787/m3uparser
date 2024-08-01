from jellyfin_apiclient_python import JellyfinClient
import os
import json
# def api_client_auth(jellyfin_url, api_key):
#     try:
#         apikey_ezpztv = JellyfinClient()
#         apikey_ezpztv.config.app('EZPZTV', '21.12', 'device', '123456')
#         apikey_ezpztv.config.data["auth.ssl"] = True
#         apikey_ezpztv.authenticate(
#             {"Servers": [
#                 {"AccessToken": api_key, "address": jellyfin_url}]}, discover=False)
#
#         return apikey_ezpztv
#
#     except Exception as e:
#         print(f"Failed to authenticate API key: {e}")
#         raise


def run_guide_task(api_key, jellyfin_url, live_tv):
    if live_tv:
        # Use api-key method to get default headers
        apikey_ezpztv = JellyfinClient()
        apikey_ezpztv.config.app('EZPZTV', '21.12', 'device', '123456')
        apikey_ezpztv.config.data["auth.ssl"] = True
        apikey_ezpztv.authenticate(
            {"Servers": [
                {"AccessToken": api_key, "address": jellyfin_url}]}, discover=False)
        try:
            headers = apikey_ezpztv.jellyfin.get_default_headers()
            # Send POST request to the specified endpoint
            response = apikey_ezpztv.jellyfin.send_request(
                jellyfin_url,
                "ScheduledTasks/Running/bea9b218c97bbf98c5dc1303bdb9a0ca",
                method="post",
                headers=headers
            )

            if response.status_code == 204:
                print("Scheduled task started successfully.")
            elif response.status_code == 401:
                raise ValueError("Invalid API key.")
            else:
                print(f"Failed to start scheduled task. Status Code: {response.status_code},"
                      f" Response: {response.content}")

        except Exception as e:
            print(f"Failed to start scheduled task: {e}")
    else:
        print("Live TV not enabled")


def run_libraryapi_task(api_key, jellyfin_url, lib_refresh):
    if lib_refresh:
        # Use api-key method to get default headers
        apikey_ezpztv = JellyfinClient()
        apikey_ezpztv.config.app('EZPZTV', '21.12', 'device', '123456')
        apikey_ezpztv.config.data["auth.ssl"] = True
        apikey_ezpztv.authenticate(
            {"Servers": [
                {"AccessToken": api_key, "address": jellyfin_url}]}, discover=False)

        try:
            headers = apikey_ezpztv.jellyfin.get_default_headers()
            # Send POST request to the specified endpoint
            response = apikey_ezpztv.jellyfin.send_request(
                jellyfin_url,
                "/Library/Refresh",
                method="post",
                headers=headers
            )

            if response.status_code == 204:
                print("Library refresh task started successfully.")
            elif response.status_code == 401:
                print("Invalid API key.")
            else:
                print(f"Failed to start Library refresh task. Status Code: {response.status_code},"
                      f" Response: {response.content}")

        except Exception as e:
            print(f"Failed to start Library refresh task: {e}")
    else:
        print(f"Library refresh is set to false, set REFRESH_LIB=true in compose file to enable")


def api_upload_log(file_path, api_key, jellyfin_url, rerun):
    # Use api-key method to get default headers
    apikey_ezpztv = JellyfinClient()
    apikey_ezpztv.config.app('EZPZTV', '21.12', 'device', '123456')
    apikey_ezpztv.config.data["auth.ssl"] = True
    apikey_ezpztv.authenticate(
        {"Servers": [
            {"AccessToken": api_key, "address": jellyfin_url}]}, discover=False)

    headers = apikey_ezpztv.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "text/plain; charset=utf-8"
    })

    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_var = file.read().replace('\\n', '\n')
    except Exception as e:
        print(f"Failed to read the log file: {e}")
        return

    headers = apikey_ezpztv.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "text/plain; charset=utf-8"
    })

    try:
        print("Uploading logs...")
        print(f"Re-run set for {rerun} hours.")
        response = apikey_ezpztv.jellyfin.send_request(
            jellyfin_url,
            "ClientLog/Document",
            method="post",
            headers=headers,
            data=log_var
        )

        if response.status_code == 200:
            print("Log was logged successfully.")
        elif response.status_code == 401:
            raise ValueError("Invalid API key.")
        else:
            print(f"Failed to add Log. Status Code: {response.status_code}, Response: {response.content}")
    except Exception as e:
        print(f"Failed to add LOG: {e}")

def add_repo_api(api_key, jellyfin_url):

    # Use api-key method to get default headers
    apikey_ezpztv = JellyfinClient()
    apikey_ezpztv.config.app('EZPZTV', '21.12', 'device', '123456')
    apikey_ezpztv.config.data["auth.ssl"] = True
    apikey_ezpztv.authenticate(
        {"Servers": [
            {"AccessToken": api_key, "address": jellyfin_url}]}, discover=False)

    try:
        headers = apikey_ezpztv.jellyfin.get_default_headers()
        headers.update({
            "Content-Type": "application/json"
        })
        addrepo = [{
                    "Name": "Jellyfin Official Repository",
                    "Url": "https://repo.jellyfin.org/files/plugin/manifest.json",
                    "Enabled": True
        }]

        # Send POST request to the specified endpoint
        response = apikey_ezpztv.jellyfin.send_request(
            jellyfin_url,
            "/Repositories",
            method="post",
            headers=headers,
            data=json.dumps(addrepo)
        )

        if response.status_code == 204:
            print("Repository added successfully.")
        elif response.status_code == 401:
            print("Invalid API key.")
        else:
            print(f"Failed to add repository. Status Code: {response.status_code},"
                  f" Response: {response.content}")

    except Exception as e:
        print(f"Failed to add repository: {e}")

# if __name__ == "__main__":
# #     run_guide_task()
