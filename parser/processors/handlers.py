import os
import shutil
import requests
from parser.utils import write_to_file


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


def handle_entry(entry, tv_dir, movies_dir, unsorted_dir, write_to_file, errors):
    try:

        if entry.get('series') and entry.get('tv_show') and not entry.get("exclude"):
            show_title = entry.get('show_title')
            season = entry.get('season')
            season_episode = entry.get('season_episode')
            series_dir = os.path.join(tv_dir, show_title, f"Season {season}")
            if not os.path.exists(series_dir):
                os.makedirs(series_dir)
                # print(f"Created directory: {series_dir}")
            strm_file = os.path.join(series_dir, f"{show_title} {season_episode}.strm")
            # print(f"Writing to file: {strm_file}")
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('television') and entry.get('tv_show') and not entry.get("exclude"):
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
            # print(f"Writing to file: {strm_file}")
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('movie') and not entry.get("exclude"):
            movie_title = entry.get('movie_title')
            movie_date = entry.get('movie_date')
            movie_dir_path = os.path.join(movies_dir, f"{movie_title} ({movie_date})")
            if not os.path.exists(movie_dir_path):
                os.makedirs(movie_dir_path)
                # print(f"Created directory: {movie_dir_path}")
            strm_file = os.path.join(movie_dir_path, f"{movie_title} ({movie_date}).strm")
            # print(f"Writing to file: {strm_file}")
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('unsorted') and not entry.get("exclude"):
            group_title = entry.get('group-title', '')
            unsorted_dir_path = os.path.join(unsorted_dir, group_title)
            if not os.path.exists(unsorted_dir_path):
                os.makedirs(unsorted_dir_path)
                # print(f"Created directory: {unsorted_dir_path}")
            strm_file = os.path.join(unsorted_dir_path, f"{group_title}.strm")
            # print(f"Writing to file: {strm_file}")
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
        strm_file = handle_entry(entry, tv_dir, movies_dir, unsorted_dir, write_to_file, errors)
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


def move_files(file_path, destination_path):
    destination_file_path = os.path.join(destination_path, os.path.basename(file_path))
    if os.path.isfile(destination_file_path):
        os.remove(destination_file_path)
        print(f"Removed existing file at {destination_file_path}")
    shutil.move(file_path, destination_path)

    print(f"Moved {file_path} to {destination_path}")


def prepare_m3us(URLS, m3u_dir, m3u_file_path, skip_header=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    for vodurl in URLS:
        try:
            # If skip_header is True, skip the header checks and download directly
            if skip_header:
                print('Skipping url header check.')
                response = requests.get(vodurl, headers=headers)
                print(f"GET request to {vodurl} returned status code: {response.status_code}")

                if response.status_code == 200:
                    # Determine the filename from the URL
                    filename = os.path.basename(vodurl)
                    file_path = os.path.join(m3u_dir, filename)

                    # Save the file content
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded file from URL: {vodurl}")
                else:
                    print(f"GET request failed for {vodurl} - Status code: {response.status_code}")
                continue  # Skip the rest of the loop for this URL and go to the next one

            # Default behavior: check headers before downloading
            response = requests.head(vodurl, headers=headers)
            print(f"HEAD response headers for {vodurl}: {response.headers}")
            print(f"HEAD request to {vodurl} returned status code: {response.status_code}")

            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                content_disposition = response.headers.get('content-disposition')

                if content_type and 'filename=' in (content_disposition or ''):
                    response = requests.get(vodurl, headers=headers)
                    print(f"GET request to {vodurl} returned status code: {response.status_code}")

                    if response.status_code == 200:
                        # Determine the filename from the URL
                        filename = os.path.basename(vodurl)
                        file_path = os.path.join(m3u_dir, filename)

                        # Save the file content
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                        print(f"Downloaded file from URL: {vodurl}")
                    else:
                        print(f"GET request failed for {vodurl} - Status code: {response.status_code}")
                else:
                    print(f"URL not valid: {vodurl} - Content-Type or filename missing. Skipping...")
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
                    if len(lines) < 2:
                        continue
                    outfile.write("\n")
                    outfile.writelines(lines)
            else:
                print(f"Cannot read {file_path}")

    print(f"All files have been combined into {m3u_file_path}")

    # Check if the combined m3u file has 3 or fewer lines
    print("Checking the combined m3u file for line count...")
    with open(m3u_file_path, 'r') as m3u_file:
        print("Reading the combined m3u file for line count...")
        lines = m3u_file.readlines()
        print(f"Lines in the combined m3u file: {len(lines)}")
        if len(lines) <= 1:
            raise ValueError(f"The m3u file {m3u_file_path} has 3 or fewer lines. Aborting.")

# def prepare_m3us(URLS, m3u_dir, m3u_file_path):
#     for vodurl in URLS:
#         try:
#             response = requests.head(vodurl)
#             print(f"HEAD response headers for {vodurl}: {response.headers}")
#             print(f"HEAD request to {vodurl} returned status code: {response.status_code}")
#
#             if response.status_code == 200:
#                 content_type = response.headers.get('Content-Type')
#                 content_disposition = response.headers.get('content-disposition')
#
#                 if content_type and 'filename=' in (content_disposition or ''):
#                     response = requests.get(vodurl)
#                     print(f"GET request to {vodurl} returned status code: {response.status_code}")
#
#                     if response.status_code == 200:
#                         # Determine the filename from the URL
#                         filename = os.path.basename(vodurl)
#                         file_path = os.path.join(m3u_dir, filename)
#
#                         # Save the file content
#                         with open(file_path, 'wb') as file:
#                             file.write(response.content)
#                         print(f"Downloaded file from URL: {vodurl}")
#                     else:
#                         print(f"GET request failed for {vodurl} - Status code: {response.status_code}")
#                 else:
#                     print(f"URL not valid: {vodurl} - Content-Type or filename missing. Skipping...")
#             else:
#                 print(f"URL is not accessible: {vodurl} - Status code: {response.status_code}")
#         except requests.RequestException as e:
#             print(f"Error processing URL {vodurl}: {e}")
#
#     print("All URLs processed.")
#
#     # Create the output file and add #EXTM3U at the beginning
#     with open(m3u_file_path, 'w') as outfile:
#         outfile.write("#EXTM3U\n")
#         # Loop through each file in the specified directory
#         for file in os.listdir(m3u_dir):
#             file_path = os.path.join(m3u_dir, file)
#             print(f"Processing file: {file_path}")
#             # Check if the file exists and is readable
#             if os.path.isfile(file_path):
#                 with open(file_path, 'r') as infile:
#                     # Skip the first line and append the rest to the output file
#                     lines = infile.readlines()[1:]
#                     if lines:
#                         outfile.write("\n")
#                         outfile.writelines(lines)
#             else:
#                 print(f"Cannot read {file_path}")
#
#     print(f"All files have been combined into {m3u_file_path}")


# sync_directories with remove from src if not in dest
def sync_directories(src, dest, remove_sync):
    if remove_sync:
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)

            if os.path.isdir(src_item):
                if not os.path.exists(dest_item):
                    os.makedirs(dest_item)
                    # print(f"Created directory: {dest_item}")
                sync_directories(src_item, dest_item, remove_sync)
            elif os.path.isfile(src_item):
                if not os.path.exists(dest_item):
                    shutil.copy2(src_item, dest_item)
                    print(f"Added content: {dest_item}")
                else:
                    # Check if contents differ
                    with open(src_item, 'rb') as f_src, open(dest_item, 'rb') as f_dest:
                        if f_src.read() != f_dest.read():
                            shutil.copy2(src_item, dest_item)
                            print(f"Updated content: {dest_item}")

        # Remove files and directories in dest that are not in src
        for item in os.listdir(dest):
            dest_item = os.path.join(dest, item)
            src_item = os.path.join(src, item)

            if not os.path.exists(src_item):
                if os.path.isdir(dest_item):
                    shutil.rmtree(dest_item)
                    print(f"Removed directory: {dest_item}")
                elif os.path.isfile(dest_item):
                    os.remove(dest_item)
                    print(f"Removed file: {dest_item}")
    else:
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)

            if os.path.isdir(src_item):
                if not os.path.exists(dest_item):
                    os.makedirs(dest_item)
                sync_directories(src_item, dest_item, remove_sync)
            elif os.path.isfile(src_item):
                if not os.path.exists(dest_item):
                    shutil.copy2(src_item, dest_item)
                    print(f"Content added: {dest_item}")
                else:
                    # Check if contents differ
                    with open(src_item, 'rb') as f_src, open(dest_item, 'rb') as f_dest:
                        if f_src.read() != f_dest.read():
                            shutil.copy2(src_item, dest_item)
                            print(f"Content updated: {dest_item}")

# def sync_directories(src, dest):
#     for item in os.listdir(src):
#         src_item = os.path.join(src, item)
#         dest_item = os.path.join(dest, item)
#
#         if os.path.isdir(src_item):
#             if not os.path.exists(dest_item):
#                 os.makedirs(dest_item)
#             sync_directories(src_item, dest_item)
#         elif os.path.isfile(src_item):
#             if not os.path.exists(dest_item):
#                 shutil.copy2(src_item, dest_item)
#                 print(f"Added content to {dest_item}")
