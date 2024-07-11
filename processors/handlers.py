import os
import shutil
import requests


def process_live_tv_entries(entries, livetv_file):
    with open(livetv_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for entry in entries:
            if entry.get('livetv'):
                extinf_line = entry.get('extinf_line', '')
                extgrp_line = entry.get('extgrp', '')
                stream_url_line = entry.get('stream_url', '')

                # Write EXTINF line
                f.write(extinf_line + '\n')

                # Write EXTGRP line
                if extgrp_line:
                    f.write(f"{extgrp_line}\n")

                # Write stream URL
                f.write(stream_url_line + '\n')


def handle_entry(entry, tv_dir, movies_dir, unsorted_dir, errors):
    try:

        if entry.get('series') and entry.get('tv_show'):
            show_title = entry.get('show_title')
            season = entry.get('season')
            season_episode = entry.get('season_episode')
            series_dir = os.path.join(tv_dir, show_title, f"Season {season}")
            if not os.path.exists(series_dir):
                os.makedirs(series_dir)
                # print(f"Created directory: {series_dir}")
            strm_file = os.path.join(series_dir, f"{show_title} {season_episode}.strm")
            print(f"Writing to file: {strm_file}")
            from utils import write_to_file
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('television') and entry.get('tv_show'):
            air_date = entry.get('air_date')
            show_title = entry.get('show_title')
            guest_star = entry.get('guest_star')
            television_file = [show_title]
            if guest_star:
                television_file.append(guest_star)
            television_file.append(air_date)
            tv_strm_file = f","' '.join(television_file)
            tv_show_dir = os.path.join(tv_dir, show_title)
            if not os.path.exists(tv_show_dir):
                os.makedirs(tv_show_dir)
                # print(f"Created directory: {tv_show_dir}")
            strm_file = os.path.join(tv_show_dir, f"{tv_strm_file}.strm")
            print(f"Writing to file: {strm_file}")
            from utils import write_to_file
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('movie'):
            movie_title = entry.get('movie_title')
            movie_date = entry.get('movie_date')
            movie_dir_path = os.path.join(movies_dir, f"{movie_title} ({movie_date})")
            if not os.path.exists(movie_dir_path):
                os.makedirs(movie_dir_path)
                # print(f"Created directory: {movie_dir_path}")
            strm_file = os.path.join(movie_dir_path, f"{movie_title} ({movie_date}).strm")
            print(f"Writing to file: {strm_file}")
            from utils import write_to_file
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('unsorted'):
            group_title = entry.get('group-title', '')
            unsorted_dir_path = os.path.join(unsorted_dir, group_title)
            if not os.path.exists(unsorted_dir_path):
                os.makedirs(unsorted_dir_path)
                # print(f"Created directory: {unsorted_dir_path}")
            strm_file = os.path.join(unsorted_dir_path, f"{group_title}.strm")
            print(f"Writing to file: {strm_file}")
            from utils import write_to_file
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

    except Exception as e:
        error_message = f"Error handling entry: {entry}\nError: {e}"
        print(error_message)
        errors.append(error_message)
        return None


def proc_entries(entries, errors, tv_dir, movies_dir, unsorted_dir):
    tv_strm_files = []
    movie_strm_files = []
    unsorted_strm_files = []
    for entry in entries:
        # from parser import tv_dir, movies_dir, unsorted_dir
        strm_file = handle_entry(entry, tv_dir, movies_dir, unsorted_dir, errors)
        if strm_file:
            if entry.get('tv_show'):
                tv_strm_files.append(strm_file)
            elif entry.get('movie'):
                movie_strm_files.append(strm_file)
            elif entry.get('unsorted'):
                unsorted_strm_files.append(strm_file)
    # Print the final parsed dictionaries
    # print("\nFinal parsed dictionaries:")
    # for d in entries:
        # print(d)


def sync_directories(src, dest):
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isdir(src_item):
            if not os.path.exists(dest_item):
                os.makedirs(dest_item)
            sync_directories(src_item, dest_item)
        elif os.path.isfile(src_item):
            if not os.path.exists(dest_item):
                shutil.copy2(src_item, dest_item)


def move_files(file_path, destination_path):
    destination_file_path = os.path.join(destination_path, os.path.basename(file_path))
    if os.path.isfile(destination_file_path):
        os.remove(destination_file_path)
        print(f"Removed existing file at {destination_file_path}")
    shutil.move(file_path, destination_path)

    print(f"Moved {file_path} to {destination_path}")


def prepare_m3us(URLS, m3u_dir, m3u_file_path):
    for vodurl in URLS:
        try:
            response = requests.head(vodurl)
            print(f"HEAD response headers for {vodurl}: {response.headers}")
            print(f"HEAD request to {vodurl} returned status code: {response.status_code}")

            if response.status_code == 200:
                response = requests.get(vodurl)
                print(f"GET request to {vodurl} returned status code: {response.status_code}")

                # Determine the filename from the URL
                filename = os.path.basename(vodurl)
                file_path = os.path.join(m3u_dir, filename)

                # Save the file content
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded file from URL: {vodurl}")
            else:
                print(f"URL is not accessible: {vodurl} - Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error processing URL {vodurl}: {e}")

    print("All URLs processed.")

    # Create the output file and add #EXTM3U at the beginning
    with open(m3u_file_path, 'w') as outfile:
        outfile.write("#EXTM3U\n")
        # Loop through each file in the specified directory
        for file in os.listdir(m3u_dir):
            file_path = os.path.join(m3u_dir, file)
            print(f"Processing file: {file_path}")
            # Check if the file exists and is readable
            if os.path.isfile(file_path):
                with open(file_path, 'r') as infile:
                    # Skip the first line and append the rest to the output file
                    lines = infile.readlines()[1:]
                    outfile.writelines(lines)
            else:
                print(f"Cannot read {file_path}")

    print(f"All files have been combined into {m3u_file_path}")
