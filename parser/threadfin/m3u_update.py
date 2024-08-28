import requests
import time


def tf_update(thread_user, thread_pass, host, port):
    try:
        # thread_url = thread_url if thread_url else "http://127.0.0.1:34400"
        host = host if host else '127.0.0.1'
        port = port if port else '34400'
        url = f"http://{host}:{port}/api/"

        headers = {
            "Content-Type": "application/json"
        }

        # Prepare login data
        login_data = {
            "cmd": "login",
            "username": thread_user,
            "password": thread_pass
        }

        try:
            # Send login request
            response = requests.post(url, headers=headers, json=login_data)
            print(f"Login Response: {response.text}")

            response_json = response.json()

            if response_json.get("status"):
                token = response_json.get("token")
            else:
                raise Exception(
                    "Threadfin Login Failed: check username, password, and url. Ensure API access is enabled,"
                    " and if API auth is also enabled, ensure that the user has API access enabled."
                )

        except requests.exceptions.RequestException as e:
            print(f"Login request failed: {e}")
            raise

        # Step 1: Prepare and send m3u update data
        update_data = {
            "cmd": "update.m3u",
            "token": token
        }
        time.sleep(10)
        try:
            response = requests.post(url, headers=headers, json=update_data)
            print(f"Update m3u Response: {response.text}")
            response_json = response.json()

            if response.status_code in [400, 403, 423]:
                print(f"Update m3u failed: {response.text}")
                return
            else:
                print("Update m3u success")
                token = response_json.get("token")  # Update token for next request

        except requests.exceptions.RequestException as e:
            print(f"Update m3u request failed: {e}")
            return
        time.sleep(10)
        # Step 2: Prepare and send XML update request
        update_xml = {
            "cmd": "update.xmltv",
            "token": token
        }

        try:
            response = requests.post(url, headers=headers, json=update_xml)
            print(f"Update XMLTV Response: {response.text}")
            response_json = response.json()

            if response.status_code in [400, 403, 423]:
                print(f"Update XMLTV failed: {response.text}")
                return
            else:
                print("Update XMLTV success")
                token = response_json.get("token")  # Update token for next request

        except requests.exceptions.RequestException as e:
            print(f"Update XMLTV request failed: {e}")
            return
        time.sleep(10)
        # Step 3: Prepare and send EPG update request
        update_epg = {
            "cmd": "update.xepg",
            "token": token
        }

        try:
            response = requests.post(url, headers=headers, json=update_epg)
            print(f"Update EPG Response: {response.text}")

            if response.status_code in [400, 403, 423]:
                print(f"Update EPG failed: {response.text}")
            else:
                print("Update EPG success")

        except requests.exceptions.RequestException as e:
            print(f"Update EPG request failed: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     tf_update('user', 'pass', 'http://127.0.0.1:34400')