import json
from websocket import create_connection
import time
import requests
from parser.config.variables import *
import re


class ThreadfinWebSocketClient:
    def __init__(self, m3u_url=None, epg_url=None, host=None, port=None, thread_user=None, thread_pass=None,
                 token=None):
        self.host = host if host else '10.21.12.9'
        self.port = port if port else '34400'
        self.m3u_url = f'./conf/data/livetv.m3u'
        self.epg = epg_url
        self.token = token
        self.ws_url = f"ws://{self.host}:{self.port}/data/"
        self.ws_token = f"ws://{self.host}:{self.port}/data/?Token={token}"
        self.thread_user = thread_user if thread_user else 'user'
        self.thread_pass = thread_pass if thread_pass else 'pass'
        self.holder = m3u_url

    def send_wizard(self, ws):
        try:
            print(self.m3u_url)
            wizard_request = {
                "wizard": {
                    "EpgSource": "XEPG",
                    "M3U": self.m3u_url,
                    "Tuner": 1,
                    "XMLTV": ""
                },
                "cmd": "saveWizard"
            }
            ws.send(json.dumps(wizard_request))
        except Exception as e:
            print(f"Error sending wizard data: {e}")

    def send_epg(self):
        for url_data in self.epg:
            try:
                name_value = re.sub(r'^https?://|[.:/]', '', url_data)
                ws = create_connection(self.ws_url)
                epg_request = {
                    "files": {
                        "xmltv": {
                            "-": {
                                "name": name_value,
                                "description": "EPG data",
                                "file.source": url_data,
                                "http_proxy.ip": "",
                                "http_proxy.port": ""
                            }
                        }
                    },
                    "cmd": "saveFilesXMLTV"
                }
                ws.send(json.dumps(epg_request))
                result = ws.recv()
                json_result = json.loads(result)
                filtered_result = {
                    "settings": json_result.get("settings")
                }
                print(json.dumps(filtered_result, indent=4))
            except Exception as e:
                print(f"Error sending EPG data: {e}")
            finally:
                ws.close()
                time.sleep(2)

    def send_user(self, ws):
        try:
            user_request = {
                "userData": {
                    "username": self.thread_user,
                    "password": self.thread_pass,
                    "confirm": self.thread_pass,
                    "authentication.web": True,
                    "authentication.pms": False,
                    "authentication.m3u": True,
                    "authentication.xml": True,
                    "authentication.api": True
                },
                "cmd": "saveNewUser"
            }
            ws.send(json.dumps(user_request))
        except Exception as e:
            print(f"Error sending user data: {e}")

    def send_settings(self, ws):
        try:
            settings_request = {
                "settings": {
                    "authentication.web": True,
                    "authentication.pms": False,
                    "authentication.xml": True,
                    "authentication.m3u": True,
                    "authentication.api": True,
                    "api": True,
                    'ignoreFilters': True,
                    "enableNonAscii": True
                },
                "cmd": "saveSettings"
            }
            ws.send(json.dumps(settings_request))
        except Exception as e:
            print(f"Error sending settings data: {e}")

    def req_format(self, ws):
        try:
            format_request = {
                "cmd": "getServerConfig"
            }
            ws.send(json.dumps(format_request))
        except Exception as e:
            print(f"Error sending format request: {e}")

    def update_m3u(self, ws, m3u_data):
        try:
            updatem3u_request = {
                "cmd": "updateFileM3U",
                "files": {
                    "m3u": m3u_data
                }
            }
            ws.send(json.dumps(updatem3u_request))
        except Exception as e:
            print(f"Error updating M3U data: {e}")

    def update_xml(self, ws, xml_data):
        try:
            updatexml_request = {
                "cmd": "updateFileXMLTV",
                "files": {
                    "xmltv": xml_data
                }
            }
            ws.send(json.dumps(updatexml_request))
        except Exception as e:
            print(f"Error updating XML data: {e}")

    def second_setting(self, ws):
        try:
            second_setting_request = {
                "settings": {
                    "xepg.replace.missing.images": True,
                    "xepg.replace.channel.title": True,
                    "dummy": True,
                    "dummyChannel": "30_Minutes"
                },
                "cmd": "saveSettings"
            }
            ws.send(json.dumps(second_setting_request))
        except Exception as e:
            print(f"Error sending second setting data: {e}")


def run_websocket_operations():
    client = vars(ThreadfinWebSocketClient, variables_all, m3u_url=None, epg_url='epg_path', port='port',
                  thread_user='main_user', thread_pass='main_pass', token=None, host='host')
    ws = create_connection(client.ws_url)
    print("WebSocket connection established.")

    try:
        # Call the send methods
        time.sleep(2)
        while True:
            ws = create_connection(client.ws_url)
            client.ws = ws
            client.send_wizard(ws)

            # Receive and process the response
            result = ws.recv()
            time.sleep(2)
            json_result = json.loads(result)

            # Extract the settings dictionary
            settings = json_result.get("settings", {})

            # Check the value of m3u in the files dictionary within settings
            m3u_value = settings.get("files", {}).get("m3u", {})

            # Print the filtered result
            filtered_result = {
                "clientInfo": json_result.get("clientInfo"),
                "data": json_result.get("data"),
                "settings": settings
            }
            print(json.dumps(filtered_result, indent=4))


            if m3u_value:
                print("Valid m3u value received. Wizard config complete.")
                break

            print("Empty or null m3u value received. Re-running send_wizard...")
            time.sleep(3)  # Delay before retrying
            ws.close()
            # Close the connection
        ws.close()
        print("WebSocket connection closed. Wizard config complete")
        time.sleep(2)
    except Exception as e:
        print(f"Error during WebSocket send_wizard operation: {e}")

    try:
        # Call the send methods
        client.send_epg()
        print("WebSocket connection closed. EPG values sent to Threadfin")
        time.sleep(2)
    except Exception as e:
        print(f"Error during WebSocket send_epg operation: {e}")

    try:
        # Reconnect and repeat for other methods
        ws = create_connection(client.ws_url)
        print("WebSocket connection re-established.")
        client.ws = ws
        time.sleep(2)
        client.send_user(ws)

        # Receive and process the response
        result = ws.recv()
        json_result = json.loads(result)

        filtered_result = {
            "settings": json_result.get("settings")
        }
        print(json.dumps(filtered_result, indent=4))

        time.sleep(15)

        ws.close()
        print("WebSocket connection closed. User config complete")
        time.sleep(2)
    except Exception as e:
        print(f"Error during WebSocket send_user operation: {e}")

    try:
        ws = create_connection(client.ws_url)
        print("WebSocket connection re-established.")
        client.ws = ws
        time.sleep(2)
        client.send_settings(ws)

        result = ws.recv()
        json_result = json.loads(result)
        time.sleep(2)
        filtered_result = {
            "settings": json_result.get("settings")
        }
        print(json.dumps(filtered_result, indent=4))
        print("Settings values sent to Threadfin")
        time.sleep(15)
    except Exception as e:
        print(f"Error during WebSocket send_settings operation: {e}")

    finally:
        if ws:
            ws.close()
        print("WebSocket connection closed. Initial config complete")


def tf_api(thread_user, thread_pass, host, port):
    # Define default values and URL

    host = host if host else '10.21.12.9'
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
        print(f"HTTP Response Status Code: {response.status_code}")

        # Check if the response was successful
        if response.status_code == 200:
            print("Login request successful.")
            # Parse the JSON response
            response_json = response.json()
            print(f"Response JSON: {response_json}")

            # Return the derived token
            token = response_json.get("token")
            print(f"Derived token: {token}")
            return token
        else:
            print(f"Login request failed with status code: {response.status_code} and response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"RequestException occurred: {e}")
        return None

    except Exception as e:
        # Handle any other exceptions
        print(f"Exception occurred during API request: {e}")
        return None


def run_reload_operations():
    token = vars(tf_api, variables_all, thread_user='main_user', thread_pass='main_pass', host='host', port='port')
    client = vars(ThreadfinWebSocketClient, variables_all, host='host', port='port', thread_user='main_user',
                  thread_pass='main_pass', token=token)
    ws = create_connection(client.ws_token)
    print("WebSocket connection established.")

    second_setting = False  # Initialize the empty_xml flag

    try:
        # Call the req_format method
        client.ws = ws
        client.req_format(ws)
        time.sleep(1)

        # Receive and process the response
        result = ws.recv()
        json_result = json.loads(result)

        # Extract and print the m3u/xmltv_data
        m3u_data = json_result['settings']['files']['m3u']
        xml_data = json_result['settings']['files']['xmltv']
        print(json.dumps(m3u_data, indent=4))
        print(f"files:{json.dumps(xml_data, indent=4)}")
        m3u_inner_data = next(iter(m3u_data.values()))
        counter_download = m3u_inner_data.get('counter.download', 0)

        if counter_download <= 1:
            second_setting = True

        time.sleep(10)

    except Exception as e:
        print(f"Error during WebSocket operation: {e}")

    finally:
        if ws:
            ws.close()
        print("WebSocket connection closed.")

    token = vars(tf_api, variables_all, thread_user='main_user', thread_pass='main_pass', host=None, port=None)
    client = vars(ThreadfinWebSocketClient, variables_all, host=None, port=None, thread_user='main_user',
                  thread_pass='main_pass', token=token)
    ws = create_connection(client.ws_token)
    print("WebSocket connection established.")
    try:
        # Call the req_format method
        client.ws = ws
        client.update_m3u(ws, m3u_data)
        ws.recv()
        print("Updated m3u file")
        time.sleep(10)
    except Exception as e:
        print(f"Error during WebSocket operation: {e}")

    finally:
        if ws:
            ws.close()
        print("WebSocket connection closed.")
        time.sleep(10)

    token = vars(tf_api, variables_all, thread_user='main_user', thread_pass='main_pass', host=None, port=None)
    client = vars(ThreadfinWebSocketClient, variables_all, host=None, port=None, thread_user='main_user',
                  thread_pass='main_pass', token=token)
    ws = create_connection(client.ws_token)
    print("WebSocket connection established.")
    try:
        # Call the update_xml method
        client.ws = ws
        client.update_xml(ws, xml_data)
        ws.recv()
        print("Updated xml/epg data")
        time.sleep(10)
    except Exception as e:
        print(f"Error during WebSocket operation: {e}")

    finally:
        if ws:
            ws.close()
        print("WebSocket connection closed.")
        time.sleep(10)

    # Conditionally run the no_xml method if empty_xml is True
    if second_setting:
        try:
            token = vars(tf_api, variables_all, thread_user='main_user', thread_pass='main_pass', host=None, port=None)
            client = vars(ThreadfinWebSocketClient, variables_all, host=None, port=None, thread_user='main_user',
                          thread_pass='main_pass', token=token)
            ws = create_connection(client.ws_token)
            print("WebSocket connection established.")
            client.ws = ws
            client.second_setting(ws)
            ws.recv()
            print("Applied dummy epg and additional settings.")
            time.sleep(10)
        except Exception as e:
            print(f"Error during WebSocket operation: {e}")

        finally:
            if ws:
                ws.close()
            print("WebSocket connection closed... re applying values with another refresh of all data.")
            time.sleep(10)

        run_reload_operations()


# Example usage
# if __name__ == "__main__":
    # run_websocket_operations()
    # tf_api('user', 'pass', thread_url=None)
    # run_reload_operations()
