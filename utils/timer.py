import time

def run_timer(main, wait_x):
    while True:
        print(f"Waiting for {wait_x} seconds before restarting...")
        time.sleep(wait_x)
        main()
