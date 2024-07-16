import time
from .errors_counters import log_shut_down


def run_timer(main, wait_x):
    while True:
        log_shut_down()
        print(f"Waiting for {wait_x} seconds before restarting...")
        time.sleep(wait_x)
        main()


def wait_for_server():
    print("Waiting for server to initialize...")
    time.sleep(21)

