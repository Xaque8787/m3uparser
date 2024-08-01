from parser.jellyfin_api.utility import ping_server, upload_log
from parser.jellyfin_api.user_clients import client_main_user
from parser.jellyfin_api.libraries import run_scheduled_task, run_library_task
from parser.config.variables import *


def ezpztv_task():
    try:
        print("Checking for server connectivity")
        value = vars(ping_server, variables_all, 'jellyfin_url', max_retries=8, interval=7)
        if value == "continue":
            main_client = vars(client_main_user, variables_all, 'jellyfin_url', 'main_user', 'main_pass')
            vars(run_scheduled_task, variables_all, main_client, 'jellyfin_url', 'live_tv')
            vars(run_library_task, variables_all, main_client, 'jellyfin_url', 'lib_refresh')
            vars(upload_log, variables_all, main_client, 'log_file', 'jellyfin_url', 'HOURS')
        else:
            exit(0)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    ezpztv_task()
