import os


def dirmake(server_cfg, cfg_file, logs, m3u_dir, livetv_file, live_tv_dir, tv_dir, movies_dir,
            unsorted_dir, log_file, branding_file):
    try:

        # Create directories if they don't exist
        for directory in [m3u_dir, live_tv_dir, logs, server_cfg, unsorted_dir, tv_dir, movies_dir, branding_file]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Ensure the livetv.m3u file starts with #EXTM3U and uses UTF-8 encoding
        if not os.path.exists(livetv_file):
            with open(livetv_file, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
        else:
            with open(livetv_file, "r+", encoding="utf-8") as f:
                if not f.readline().startswith("#EXTM3U"):
                    content = f.read()
                    f.seek(0, 0)
                    f.write("#EXTM3U\n" + content)

        if not os.path.exists(cfg_file):
            with open(cfg_file, "w", encoding="utf-8") as f:
                f.write("SERVER_SETUP=False")

        if not os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("logging")
        else:
            pass
    except Exception as e:
        print(f"An error occurred: {e}")
