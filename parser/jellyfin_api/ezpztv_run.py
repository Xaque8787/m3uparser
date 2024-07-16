from parser.jellyfin_api.utility import server_init, logs
from parser.jellyfin_api.user_clients import user_mgmt
from parser.jellyfin_api.libraries import library_mgmt
from parser.jellyfin_api.utility.server_init import live_tv, log_file_path


def ezpztv_task():
    try:
        value = server_init.ping_server(max_retries=8, interval=7)
        if value == "continue":
            main_client = user_mgmt.client_main_user()
            logs.upload_log(log_file_path, main_client)
            if live_tv:
                library_mgmt.run_scheduled_task(main_client)

        else:
            exit(0)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    ezpztv_task()
