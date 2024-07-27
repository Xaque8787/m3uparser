import time
from .errors_counters import log_shut_down


def run_timer(main, wait_x):
    while True:
        log_shut_down()
        wait_time = int(wait_x) * 3600
        print(f"Waiting for {wait_time} seconds before restarting...")
        time.sleep(wait_time)
        main()

def wait_for_server(wait_t):
    print("Waiting for server to initialize...")
    time.sleep(wait_t)
