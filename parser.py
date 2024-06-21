import re
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
m3u_file_path = os.path.join(script_dir, "m3u_file.m3u")
# Initialize directories
tv_dir = os.path.join(script_dir, "TV VOD")
movies_dir = os.path.join(script_dir, "Movie VOD")
unsorted_dir = os.path.join(script_dir, "Unsorted VOD")
livetv_file = os.path.join(script_dir, "livetv.m3u")
# Create directories if they don't exist
for directory in [tv_dir, movies_dir, unsorted_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)
# Ensure the livetv.m3u file starts with #EXTM3U and use UTF-8 encoding
if not os.path.exists(livetv_file):
    with open(livetv_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
else:
    with open(livetv_file, "r+", encoding="utf-8") as f:
        if not f.readline().startswith("#EXTM3U"):
            f.seek(0, 0)
            content = f.read()
            f.seek(0, 0)
            f.write("#EXTM3U\n" + content)

def extract_key_value_pairs(line):
    # Define the regular expression pattern for key=value pairs
    pattern = r'(\w[\w-]*?)="(.*?)"'
    
    # Find all matches in the string
    matches = re.finditer(pattern, line)

    result = {}
    last_end = 0
    last_key = None

    
    for match in matches:
        key = match.group(1).strip()
        value = match.group(2).strip()
        result[key] = value

        if last_key is not None:
            # Add any text between the previous key-value pair and this key-value pair to the last key's value
            result[last_key] += line[last_end:match.start()].strip()
        last_key = key
        last_end = match.end()

    if last_key is not None:
        # Add any remaining text to the last key's value
        result[last_key] += line[last_end:].strip()

    # Extract EXTINF line
    extinf_match = re.search(r'^#EXTINF:.+$', line)
    if extinf_match:
        result['extinf_line'] = extinf_match.group(0)

    
    # Extract duration from #EXTINF line
    duration_match = re.search(r'^#EXTINF:(-?\d*)\s', line)
    if duration_match:
        duration = duration_match.group(1)
        result['duration'] = duration if duration else ''
    # Extract resolution from #EXTINF line
    resolution_match = re.search(r'.*?\b(HD|SD)\s*', line)
    if resolution_match:
        result['resolution'] = resolution_match.group(1)  
    
    return result


def read_remove_strings(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


remove_strings_file = './vars/removal.txt'
remove_strings = read_remove_strings(remove_strings_file)


def read_remove_header(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

remove_header_file = './vars/header.txt'
remove_header = read_remove_header(remove_header_file)

def read_terms_file(file_path):
    with open(file_path, 'r') as file:
        terms = file.read().splitlines()
    return terms


remove_terms_file = './vars/terms.txt'
remove_terms = read_terms_file(remove_terms_file)

def process_value(value, remove_strings=None, remove_header=None, remove_terms=None):
    #print("Initial value:", value)
    processed_strings = set()

    if remove_strings:
        for remove_string in remove_strings:
            if remove_string in processed_strings:
                continue

            #print("\nProcessing remove_string:", remove_string)
            pattern = re.compile(r'(\b{}\b\S*)\b(?!.*\b{}\b)'.format(re.escape(remove_string), re.escape(remove_string)), flags=re.IGNORECASE)
            match = pattern.search(value)
            if match:
                #print("Match found:", match.group(0))
                value = value[:match.start()] + value[match.end():]
                #print("Value after removal:", value)
                processed_strings.add(remove_string)
            else:
                #print("No match found")
                pass

    if remove_header:
        for header_term in remove_header:
            #print("\nProcessing header term from header.txt:", header_term)
            pattern = re.compile(r'.*?\b{}\s*'.format(re.escape(header_term)), flags=re.IGNORECASE)
            match = pattern.search(value)
            if match:
                value = value[match.end():].strip()
                #print("Value after {} removal:".format(header_term), value)
            else:
                #print("Header term {} not found in value".format(header_term))
                pass

    if remove_terms:
        for terms_term in remove_terms:
            #print("\nProcessing terms term from terms.txt:", terms_term)
            pattern = re.compile(r'\s*{}\S*'.format(re.escape(terms_term)))
            match = pattern.search(value)
            if match:
                value = pattern.sub('', value).strip()
                #print("Value after {} removal:".format(terms_term), value)
            else:
                #print("Term {} not found in value".format(terms_term))
                pass  

    print("Final value:", value)
    return value.strip()

def process_strings(value, remove_strings=None, remove_header=None, remove_terms=None):
    if remove_strings:
        value = process_value(value, remove_strings=remove_strings)
    if remove_header:
        value = process_value(value, remove_header=remove_header)
    if remove_terms:
        value = process_value(value, remove_terms=remove_terms)
    return value

clean_movies = False
clean_series = False
clean_tv = False
clean_unsorted = False

def enable_cleaners(file_path):
    global clean_movies, clean_series, clean_tv, clean_unsorted
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split('=')
                key = key.strip()
                value = value.strip().lower() == 'true'
                if key == 'movies':
                    clean_movies = value
                if key == 'series':
                    clean_series = value
                if key == 'tv':
                    clean_tv = value
                if key == 'unsorted':
                    clean_unsorted = value

file_path = './vars/cleaners.txt'
enable_cleaners(file_path)


def clean_group_title(entry):
    value = entry.get('group-title', '')
    print(f"Original group-title value: {value}")
    
     
    # Check if it's a TV show and extract season_episode and air_date
    season_episode_match = re.search(r'\b[sS]\d{1,3}[eE]\d{1,3}\b|\b[0-9]{1,3}[xX][0-9]{1,3}\b|\b[sS]\d{1,3}[eE]\d{1,3}\b', value)
    if season_episode_match:
        entry['season_episode'] = season_episode_match.group(0).strip()
        entry['series'] = True
        entry['tv_show'] = True
        show_title_match = re.search(r'.*?(?=\b[sS]\d{1,3}[eE]\d{1,3}\b|\b[0-9]{1,3}[xX][0-9]{1,3}\b|\b[sS]\d{1,3}[eE]\d{1,3}\b)', value)
        if show_title_match:
            show_title = show_title_match.group(0).strip()
            if clean_series:
                entry['show_title'] = process_value(show_title_match.group(0), remove_terms=remove_terms).strip()
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
    show_title_match = re.search(r'.*?(?=\b(?:19\d{2} \d{2} \d{2}|20\d{2} \d{2} \d{2}|\d{2} \d{2} 19\d{2}|\d{2} \d{2} 20\d{2}))\b', value)
    if show_title_match:
        entry['show_title'] = show_title_match.group(0).strip()
        value = re.sub(re.escape(entry['show_title']), '', value).strip()
    air_date_match = re.search(r'\b(?:19\d{2} \d{2} \d{2}|20\d{2} \d{2} \d{2}|\d{2} \d{2} 19\d{2}|\d{2} \d{2} 20\d{2})\b', value)
    if air_date_match:
        entry['air_date'] = air_date_match.group(0).strip()
        value = re.sub(re.escape(entry['air_date']), '', value).strip()
        entry['television'] = True
        entry['tv_show'] = True
        if clean_tv:
            value = process_value(value, remove_terms=remove_terms).strip()
            entry['guest_star'] = value.strip()
            value = re.sub(re.escape(entry['guest_star']), '', value).strip()
        else:
            entry['guest_star'] = value.strip()
            value = re.sub(re.escape(entry['guest_star']), '', value).strip()
    # Check if it's a Movie and extract movie_date
    if 'tv_show' not in entry:
        movie_title_match = re.search(r'(.*?)(?=\S*\b(?:19[0-9]{2}|20[0-9]{2})\b\S*(?!.*\b(?:19[0-9]{2}|20[0-9]{2})\b))', value)
        if movie_title_match:
            movie_title = movie_title_match.group(1).strip()
            if clean_movies:
                entry['movie_title'] = process_value(movie_title_match.group(1), remove_terms=remove_terms).strip()
                entry['movie'] = True
                value = re.sub(re.escape(entry['movie_title']), '', value).strip()
            else:
                entry['movie_title'] = movie_title
                entry['movie'] = True
                value = re.sub(re.escape(entry['movie_title']), '', value).strip()
    # Movie Date Extraction
        movie_date_match = re.search(r'\b(19[0-9][0-9]|\(19[3-9][0-9]\)|20[0-9][0-9]|\(20[0-9][0-9]\))\b(?!.*\b(19[0-9][0-9]|\(19[3-9][0-9]\)|20[0-9][0-9]|\(20[0-9][0-9]\))\b)' , value)
        if movie_date_match:
            entry['movie_date'] = movie_date_match.group(0).strip()
            value = re.sub(re.escape(entry['movie_date']), '', value).strip()
                        
    # Determine if it's Live TV based on duration
    if 'movie' not in entry and 'tv_show' not in entry and 'duration' in entry and entry['duration'] == '-1':
        entry['livetv'] = True

    # Set entry of 'unsorted'
    if 'movie' not in entry and 'tv_show' not in entry and 'livetv' not in entry:
        entry['unsorted'] = True
    
    # Determine unsorted type if possible
    #if 'unsorted' in entry:
    #season_match = re.search(r'(?<=[sS])\d{1,3}|\d{1,3}(?=[xX])', entry['season_episode'])
    #episode_matches = re.findall(r'(?<=[eE])\d{1,3}|(?<=[xX])\d{1,3}', entry['season_episode'])
        # season/episode match for 2 episodes combined ie S24E11E12
        # remove trailing numbers '0000'        
    
    # Cleaned 'group-title' value
    entry['group-title'] = value.strip()

def write_to_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

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

def parse_m3u_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    i = 0
    total_lines = len(lines)
    parsed_dictionaries = []
    errors = []

    while i < total_lines:
        line = lines[i].strip()

        # Check if the line starts with #EXTINF
        if line.startswith("#EXTINF"):
            try:
                # Extract key=value pairs from the #EXTINF line and remove header value(s)
                key_value_pairs = extract_key_value_pairs(line)
                if 'group-title' in key_value_pairs:
                    key_value_pairs['group-title'] = process_strings(key_value_pairs['group-title'], remove_header=remove_header)
                # Check if the next line is #EXTGRP or a URL
                if i + 1 < total_lines and lines[i + 1].startswith("#EXTGRP"):
                    key_value_pairs['extgrp'] = lines[i + 1].strip()
                    i += 1  # Move to the next line

                # Check if the next line is a URL
                if i + 1 < total_lines and not lines[i + 1].startswith("#EXTINF"):
                    key_value_pairs['stream_url'] = lines[i + 1].strip()
                    i += 1  # Move to the next line

                
                clean_group_title(key_value_pairs)
                parsed_dictionaries.append(key_value_pairs)

            except Exception as e:
                error_message = f"Error processing line: {line}\nError: {e}"
                print(error_message)
                errors.append(error_message)

        i += 1

    return parsed_dictionaries, errors

def handle_entry(entry, tv_dir, movies_dir, unsorted_dir, errors):
    try:
        
        
        if entry.get('series') and entry.get('tv_show'):
            show_title = entry.get('show_title')
            season = entry.get('season')
            season_episode = entry.get('season_episode')
            series_dir = os.path.join(tv_dir, show_title, f"Season {season}")
            if not os.path.exists(series_dir):
                os.makedirs(series_dir)
                #print(f"Created directory: {series_dir}")
            strm_file = os.path.join(series_dir, f"{show_title} {season_episode}.strm")
            print(f"Writing to file: {strm_file}")
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
            tv_strm_file = ' '.join(television_file)
            tv_show_dir = os.path.join(tv_dir, show_title)
            if not os.path.exists(tv_show_dir):
                os.makedirs(tv_show_dir)
                #print(f"Created directory: {tv_show_dir}")
            strm_file = os.path.join(tv_show_dir, f"{tv_strm_file}.strm")
            print(f"Writing to file: {strm_file}")
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('movie'):
            movie_title = entry.get('movie_title')
            movie_date = entry.get('movie_date')
            movie_dir_path = os.path.join(movies_dir, f"{movie_title} ({movie_date})")
            if not os.path.exists(movie_dir_path):
                os.makedirs(movie_dir_path)
                #print(f"Created directory: {movie_dir_path}")
            strm_file = os.path.join(movie_dir_path, f"{movie_title} ({movie_date}).strm")
            print(f"Writing to file: {strm_file}")
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        elif entry.get('unsorted'):
            group_title = entry.get('group-title', '')
            unsorted_dir_path = os.path.join(unsorted_dir, group_title)
            if not os.path.exists(unsorted_dir_path):
                os.makedirs(unsorted_dir_path)
                #print(f"Created directory: {unsorted_dir_path}")
            strm_file = os.path.join(unsorted_dir_path, f"{group_title}.strm")
            print(f"Writing to file: {strm_file}")
            write_to_file(strm_file, entry.get('stream_url', ''))
            return strm_file

        
    except Exception as e:
        error_message = f"Error handling entry: {entry}\nError: {e}"
        print(error_message)
        errors.append(error_message)
        return None
    
def count_strm_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".strm"):
                count += 1
    return count

def main():
    # Parse the m3u file and get a list of dictionaries containing key-value pairs
    entries, errors = parse_m3u_file(m3u_file_path)

    # Print the final parsed dictionaries
    print("\nFinal parsed dictionaries:")
    for d in entries:
        print(d)

    # Process each entry dictionary and track created .strm files
    tv_strm_files = []
    movie_strm_files = []
    unsorted_strm_files = []
    for entry in entries:
        strm_file = handle_entry(entry, tv_dir, movies_dir, unsorted_dir, errors)
        if strm_file:
            if entry.get('tv_show'):
                tv_strm_files.append(strm_file)
            elif entry.get('movie'):
                movie_strm_files.append(strm_file)
            elif entry.get('unsorted'):
                unsorted_strm_files.append(strm_file)

    # Extract live TV entries and process them separately
    live_tv_entries = [entry for entry in entries if entry.get('livetv')]
    process_live_tv_entries(live_tv_entries, livetv_file)

    # Count .strm files and live TV channels
    tv_strm_count = count_strm_files(tv_dir)
    movie_strm_count = count_strm_files(movies_dir)
    unsorted_strm_count = count_strm_files(unsorted_dir)
    livetv_channels_count = len(live_tv_entries)

    # Output errors if any
    if errors:
        print("\nTotal number of errors:", len(errors))
        for error in errors:
            print(error)


    # Output results
    print("\nTotal number of errors:", len(errors))
    print("\nNumber of movies parsed =", movie_strm_count)
    print("Number of episodes parsed =", tv_strm_count)
    print("Number of unsorted entries parsed =", unsorted_strm_count)
    print("Number of live TV channels parsed =", livetv_channels_count)


if __name__ == "__main__":
    main()
