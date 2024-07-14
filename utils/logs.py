import os
from parser.utils.server_init import jellyfin_url

def upload_log(file_path, main_client):
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_var = file.read().replace('\\n', '\n')
    except Exception as e:
        print(f"Failed to read the log file: {e}")
        return

    headers = main_client.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "text/plain; charset=utf-8"
    })

    try:
        response = main_client.jellyfin.send_request(
            jellyfin_url,
            "ClientLog/Document",
            method="post",
            headers=headers,
            data=log_var
        )

        if response.status_code == 200:
            print("Log was logged successfully.")
        else:
            print(f"Failed to add Log. Status Code: {response.status_code}, Response: {response.content}")

    except Exception as e:
        print(f"Failed to add LOG: {e}")
