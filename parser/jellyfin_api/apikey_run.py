from parser.utils import wait_for_server
from parser.jellyfin_api.utility import (ping_server, run_library_task, run_guide_task, api_upload_log)
from parser.config.variables import *


def apikey_run():
    try:
        value = vars(ping_server, variables_all, 'jellyfin_url', max_retries=8, interval=7)
        if value == "continue":
            wait_for_server(12)
            print("Running guide task")
            vars(run_guide_task, variables_all, 'APIKEY', 'jellyfin_url', 'live_tv')
            print("Running library task")
            vars(run_library_task, variables_all, 'APIKEY', 'jellyfin_url', 'lib_refresh')
            print("Upload logs")
            vars(api_upload_log, variables_all, 'log_file', 'APIKEY', 'jellyfin_url')
    except Exception as e:
        print(f"Failed to authenticate API-key: {e}")


# if __name__ == "__main__":
    # apikey_run()
