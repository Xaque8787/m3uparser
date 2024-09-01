import re
import shutil
import os
from parser.config import process_env_variable, cleaner_value


def clean_group_title(entry, REMOVE_TERMS, REMOVE_DEFAULTS):
    value = entry.get('group-title', '')
    # print(f"Original group-title value: {value}")
    combined_cleaners = cleaner_value(process_env_variable)
    cleaners = enable_cleaners(combined_cleaners)
    try:
        # Check if it's a TV show and extract season_episode and air_date
        season_episode_match = re.search(
            r'\b[sS]\d{1,3}[eE]\d{1,3}\b|\b[0-9]{1,3}[xX][0-9]{1,3}\b|\b[sS]\d{1,3}[eE]\d{1,3}\b', value)
        if season_episode_match:
            entry['season_episode'] = season_episode_match.group(0).strip()
            entry['series'] = True
            entry['tv_show'] = True
            show_title_match = re.search(
                r'.*?(?=\b[sS]\d{1,3}[eE]\d{1,3}\b|\b[0-9]{1,3}[xX][0-9]{1,3}\b|\b[sS]\d{1,3}[eE]\d{1,3}\b)', value)
            if show_title_match:
                show_title = show_title_match.group(0).strip()
                if cleaners['clean_series']:
                    entry['show_title'] = process_value(show_title_match.group(0),
                                                        remove_terms=REMOVE_TERMS + REMOVE_DEFAULTS).strip()
                    value = re.sub(re.escape(entry['show_title']), '', value).strip()
                else:
                    entry['show_title'] = show_title
                    value = re.sub(re.escape(entry['show_title']), '', value).strip()
            # Extract season and episode numbers
            season_match = re.search(r'(?<=[sS])\d{1,3}|\d{1,3}(?=[xX])', entry['season_episode'])
            episode_match = re.search(r'(?<=[eE])\d{1,3}|(?<=[xX])\d{1,3}|(?<=[eE])\d{1,4}', entry['season_episode'])
            if season_match:
                entry['season'] = season_match.group(0).strip()
            if episode_match:
                entry['episode'] = episode_match.group(0).strip()
            value = re.sub(re.escape(entry['season_episode']), '', value).strip()
        # Extract show title before air_date match
        show_title_match = re.search(
            r'.*?(?=\b(?:19\d{2} \d{2} \d{2}|20\d{2} \d{2} \d{2}|\d{2} \d{2} 19\d{2}|\d{2} \d{2} 20\d{2}))\b', value)
        if show_title_match:
            entry['show_title'] = show_title_match.group(0).strip()
            value = re.sub(re.escape(entry['show_title']), '', value).strip()
        air_date_match = re.search(
            r'\b(?:19\d{2} \d{2} \d{2}|20\d{2} \d{2} \d{2}|\d{2} \d{2} 19\d{2}|\d{2} \d{2} 20\d{2})\b', value)
        if air_date_match:
            entry['air_date'] = air_date_match.group(0).strip()
            value = re.sub(re.escape(entry['air_date']), '', value).strip()
            entry['television'] = True
            entry['tv_show'] = True
            if cleaners['clean_tv']:
                value = process_value(value, remove_terms=REMOVE_TERMS + REMOVE_DEFAULTS).strip()
                entry['guest_star'] = value.strip()
                value = re.sub(re.escape(entry['guest_star']), '', value).strip()
            else:
                entry['guest_star'] = value.strip()
                value = re.sub(re.escape(entry['guest_star']), '', value).strip()
        # Check if it's a Movie and extract movie_date
        if 'tv_show' not in entry:
            movie_title_match = re.search(
                r'(.*?)(?=\S*\b(?:19[0-9]{2}|20[0-9]{2})\b\S*(?!.*\b(?:19[0-9]{2}|20[0-9]{2})\b))', value)
            if movie_title_match:
                movie_title = movie_title_match.group(1).strip()
                if cleaners['clean_movies']:
                    entry['movie_title'] = process_value(movie_title_match.group(1), remove_terms=REMOVE_TERMS + REMOVE_DEFAULTS).strip()
                    entry['movie'] = True
                    value = re.sub(re.escape(entry['movie_title']), '', value).strip()
                else:
                    entry['movie_title'] = movie_title
                    entry['movie'] = True
                    value = re.sub(re.escape(entry['movie_title']), '', value).strip()

            # Movie Date Extraction
            movie_date_match = re.search(
                r'\b(19[0-9][0-9]|\(19[3-9][0-9]\)|20[0-9][0-9]|\(20[0-9][0-9]\))\b(?!.*\b(19[0-9][0-9]|\(19[3-9][0-9]\)|20[0-9][0-9]|\(20[0-9][0-9]\))\b)',
                value)
            if movie_date_match:
                entry['movie_date'] = movie_date_match.group(0).strip()
                value = re.sub(re.escape(entry['movie_date']), '', value).strip()

        # Determine if it's Live TV based on duration
        if 'movie' not in entry and 'tv_show' not in entry and 'duration' in entry and entry['duration'] == '-1':
            entry['livetv'] = True

            # Check if 'tvg-id' exists in the entry
            if 'tvg-id' in entry:
                tvg_id = entry['tvg-id']

                # Check if 'tvg-id' is empty/null
                if not tvg_id:
                    # Create new tvg-id from 'tvg-name' and last 3 characters of 'stream_url'
                    tvg_name = entry.get('tvg-name', '')
                    stream_url = entry.get('stream_url', '')

                    # Replace spaces and colons in 'tvg-name' with periods
                    derived_tvg_id = (
                        tvg_name.replace(' ', '.')
                        .replace(':', '.')
                        .replace('(', '.')
                        .replace(')', ".")
                        .replace('..', ".")
                        .strip('.')
                    )

                    # Append the last 3 characters of 'stream_url' with a period
                    if len(stream_url) >= 3:
                        derived_tvg_id += f".{stream_url[-3:]}"

                    # Update 'tvg-id' in the entry
                    entry['tvg-id'] = derived_tvg_id

                    # Update 'extinf_line' to replace the null tvg-id with the new value
                    extinf_line = entry.get('extinf_line', '')
                    updated_extinf_line = re.sub(r'tvg-id="[^"]*"', f'tvg-id="{derived_tvg_id}"', extinf_line)
                    entry['extinf_line'] = updated_extinf_line
        # Set entry of 'unsorted'
        if 'movie' not in entry and 'tv_show' not in entry and 'livetv' not in entry:
            entry['unsorted'] = True

        # Determine unsorted type if possible
        # if 'unsorted' in entry:
        # season_match = re.search(r'(?<=[sS])\d{1,3}|\d{1,3}(?=[xX])', entry['season_episode'])
        # episode_matches = re.findall(r'(?<=[eE])\d{1,3}|(?<=[xX])\d{1,3}', entry['season_episode'])
        # season/episode match for 2 episodes combined ie S24E11E12
        # remove trailing numbers '0000'

        # Cleaned 'group-title' value
        entry['group-title'] = value.strip()
        # final_value = entry.get('group-title', '')
        # print(f"Final group-title value: {final_value}")
    except Exception as e:
        entry['error'] = str(e)


def process_value(value, replace=None, remove_header=None, remove_terms=None):
    # Print initial value
    # print("Initial value:", value)

    if replace:
        for key, value_to_replace in replace.items():
            pattern = re.compile(re.escape(key))
            match = pattern.search(value)
            # print("\nProcessing replace term from replace values:", key)
            if match:
                value = pattern.sub(value_to_replace, value)
                # print("Value after {} replace: {}".format(key, value_to_replace), value)
            else:
                # print("Replace value {} not found in value".format(key))
                pass

    if remove_header:
        for header_term in remove_header:
            # print("\nProcessing header term from header value:", header_term)
            pattern = re.compile(r'.*?\b{}\s*'.format(re.escape(header_term)), flags=re.IGNORECASE)
            match = pattern.search(value)
            if match:
                value = value[match.end():].strip()
                # print("Value after {} removal:".format(header_term), value)
            else:
                # print("Header term {} not found in value".format(header_term))
                pass

    if remove_terms:
        for term in remove_terms:
            # print("\nProcessing terms from remove terms:", term)
            pattern = re.compile(r'\s*{}\S*'.format(re.escape(term)))
            match = pattern.search(value)
            if match:
                value = pattern.sub('', value).strip()
                # print("Value after {} removal:".format(term), value)
            else:
                # print("Term {} not found in value".format(terms_term))
                pass

    # Print final value
    # print("Final value:", value)
    return value.strip()


def enable_cleaners(cleaners_list):
    # Initialize all possible cleaners with False
    cleaners = {
        'clean_movies': False,
        'clean_series': False,
        'clean_tv': False,
        'clean_unsorted': False
    }

    # Update the values based on the cleaners_list
    for cleaner in cleaners_list:
        if cleaner == 'movies':
            cleaners['clean_movies'] = True
        elif cleaner == 'series':
            cleaners['clean_series'] = True
        elif cleaner == 'tv':
            cleaners['clean_tv'] = True
        elif cleaner == 'unsorted':
            cleaners['clean_unsorted'] = True

    return cleaners


def clean_up(m3u_dir, m3u_file_path, master_mov_dir, master_tv_dir, master_unsorted, live_tv, livetv_file,
             live_tv_dir, UNSORTED, local_unsorted, folders_to_remove=None, files_to_remove=None,
             directory_to_clean=None):

    if directory_to_clean is None:
        directory_to_clean = m3u_dir
    if files_to_remove is None:
        files_to_remove = [m3u_file_path]
    if folders_to_remove is None:
        folders_to_remove = [master_mov_dir, master_tv_dir, master_unsorted]
    if live_tv is False:
        files_to_remove.append(livetv_file)
        folders_to_remove.append(live_tv_dir)
    if UNSORTED is False:
        folders_to_remove.append(local_unsorted)

    # Remove folders and their contents
    for folder in folders_to_remove:
        try:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)
                print(f"Removed folder and its contents: {folder}")
            else:
                print(f"Folder does not exist or is not a directory: {folder}")
        except Exception as e:
            print(f"Error removing folder {folder}: {e}")

    # Remove specific files
    for file in files_to_remove:
        try:
            if os.path.exists(file) and os.path.isfile(file):
                os.remove(file)
                print(f"Removed file: {file}")
            else:
                print(f"File does not exist or is not a regular file: {file}")
        except Exception as e:
            print(f"Error removing file {file}: {e}")

    # Remove all files from a directory but keep the directory itself
    if os.path.exists(directory_to_clean) and os.path.isdir(directory_to_clean):
        try:
            for file in os.listdir(directory_to_clean):
                file_path = os.path.join(directory_to_clean, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed file from directory: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Removed folder and its contents from directory: {file_path}")
        except Exception as e:
            print(f"Error cleaning directory {directory_to_clean}: {e}")
    else:
        print(f"Directory does not exist or is not a directory: {directory_to_clean}")
