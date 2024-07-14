import re


def parse_m3u_file(m3u_file_path, clean_group_title, process_value, REPLACE_TERMS, REPLACE_DEFAULTS, SCRUB_HEADER,
                   SCRUB_DEFAULTS, REMOVE_TERMS, REMOVE_DEFAULTS):
    try:
        with open(m3u_file_path, 'r', encoding='utf-8') as file:
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
                    key_value_pairs['group-title'] = process_value(key_value_pairs['group-title'],
                                                                   remove_header=SCRUB_DEFAULTS)
                    key_value_pairs['group-title'] = process_value(key_value_pairs['group-title'],
                                                                   remove_header=SCRUB_HEADER)
                    key_value_pairs['group-title'] = process_value(key_value_pairs['group-title'],
                                                                   replace=REPLACE_DEFAULTS)
                    key_value_pairs['group-title'] = process_value(key_value_pairs['group-title'],
                                                                   replace=REPLACE_TERMS)
                # Check if the next line is #EXTGRP or a URL
                if i + 1 < total_lines and lines[i + 1].startswith("#EXTGRP"):
                    key_value_pairs['extgrp'] = lines[i + 1].strip()
                    i += 1  # Move to the next line

                # Check if the next line is a URL
                if i + 1 < total_lines and not lines[i + 1].startswith("#EXTINF"):
                    key_value_pairs['stream_url'] = lines[i + 1].strip()
                    i += 1  # Move to the next line

                clean_group_title(key_value_pairs, REMOVE_TERMS, REMOVE_DEFAULTS)
                parsed_dictionaries.append(key_value_pairs)

            except Exception as e:
                error_message = f"Error processing line: {line}\nError: {e}"
                print(error_message)
                errors.append(error_message)

        i += 1

    return parsed_dictionaries, errors


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
