import os
def dirmake(create_vars):
    try:
        create = create_vars()
        # Create directories if they don't exist
        for directory in [create['m3u_dir'], create['live_tv_dir'], create['logs'], create['server_cfg'],
                          create['unsorted_dir'], create['tv_dir'], create['movies_dir']]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Ensure the livetv.m3u file starts with #EXTM3U and uses UTF-8 encoding
        if not os.path.exists(create['livetv_file']):
            with open(create['livetv_file'], "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
        else:
            with open(create['livetv_file'], "r+", encoding="utf-8") as f:
                if not f.readline().startswith("#EXTM3U"):
                    content = f.read()
                    f.seek(0, 0)
                    f.write("#EXTM3U\n" + content)

        if not os.path.exists(create['cfg_file']):
            with open(create['cfg_file'], "w", encoding="utf-8") as f:
                f.write("SERVER_SETUP=False")
        else:
            pass
    except Exception as e:
        print(f"An error occurred: {e}")


