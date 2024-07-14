from dotenv import load_dotenv
import os


# Process functions for environment variables
def process_env_variable(env_var_value):
    return [item.strip() for item in env_var_value.strip('"').split(',') if item.strip()]


def str_to_bool(value):
    if isinstance(value, str):
        return value.lower() in ("yes", "true", "t", "1")
    return bool(value)


def process_env_special(env_var_value):
    key_value_pairs = {}

    for pair in env_var_value.split(','):
        if '=' in pair:
            key, value = pair.split('=')
            # Decode Unicode escapes in the value
            value = value.encode().decode('unicode_escape')
            key_value_pairs[key.strip()] = value.strip()

    return key_value_pairs


# Environment variables


def initialize_vars(process_env_variable, str_to_bool, process_env_special, *args):
    script_dir = os.path.dirname(os.path.dirname(__file__))
    cfg_file = os.path.join(script_dir, f'server_cfg/server.cfg')
    load_dotenv(cfg_file)
    variables = {
        'script_dir': os.path.dirname(os.path.dirname(__file__)),
        'server_cfg': os.path.join(script_dir, "server_cfg"),
        'cfg_file': os.path.join(script_dir, f'server_cfg/server.cfg'),
        'logs': os.path.join(script_dir, "logs"),
        'local_mov_dir': f'{script_dir}/VODS/Movie_VOD',
        'master_mov_dir': f'{script_dir}/Movie_VOD',
        'local_tv_dir': f'{script_dir}/VODS/TV_VOD',
        'master_tv_dir': f'{script_dir}/TV_VOD',
        'master_unsorted': f'{script_dir}/Unsorted_VOD',
        'local_unsorted': f'{script_dir}/VODS/Unsorted_VOD',
        'm3u_dir': os.path.join(script_dir, "m3u"),
        'm3u_file_path': os.path.join(script_dir, "m3u_file.m3u"),
        'livetv_file': os.path.join(script_dir, "livetv.m3u"),
        'live_tv_dir': os.path.join(script_dir, f'VODS/Live_TV'),
        'tv_dir': os.path.join(script_dir, "TV_VOD"),
        'movies_dir': os.path.join(script_dir, "Movie_VOD"),
        'unsorted_dir': os.path.join(script_dir, "Unsorted_VOD"),
        'HOURS': os.getenv('HOURS', ""),
        'URLS': process_env_variable(os.getenv('M3U_URL', "")),
        'main_user': os.getenv('USER_NAME', ""),
        'main_pass': os.getenv('PASSWORD', ""),
        'SCRUB_HEADER': process_env_variable(os.getenv('SCRUB_HEADER', "")),
        'SCRUB_DEFAULTS': process_env_variable(os.getenv('SCRUB_DEFAULTS', "")),
        'REMOVE_TERMS': process_env_variable(os.getenv('REMOVE_TERMS', "")),
        'REMOVE_DEFAULTS': process_env_variable(os.getenv('REMOVE_DEFAULTS', "")),
        'REPLACE_TERMS': process_env_special(os.getenv('REPLACE_TERMS', "")),
        'REPLACE_DEFAULTS': process_env_special(os.getenv('REPLACE_DEFAULTS', "")),
        'CLEANERS': process_env_variable(os.getenv('CLEANERS', "")),
        'CLEANERS_DEFAULTS': process_env_variable(os.getenv('CLEANERS_DEFAULTS', "")),
        'UNSORTED': str_to_bool(os.getenv('UNSORTED', "")),
        'jellyfin_url': os.getenv('JELLYFIN_URL', ""),
        'epg_path': os.getenv('EPG_URL', ""),
        'server_name': os.getenv('SERVER_NAME', ""),
        'live_tv': str_to_bool(os.getenv('LIVE_TV', "")),
        'SERVER_CFG': str_to_bool(os.getenv('SERVER_SETUP', ""))

    }

    if args:
        # Return only specified variables
        return {arg: variables[arg] for arg in args if arg in variables}
    else:
        # Return all variables
        return variables


def vars_position(process_env_variable, str_to_bool, process_env_special, *args):
    script_dir = os.path.dirname(os.path.dirname(__file__))
    cfg_file = os.path.join(script_dir, f'server_cfg/server.cfg')
    load_dotenv(cfg_file)
    variables = {
        'script_dir': os.path.dirname(os.path.dirname(__file__)),
        'server_cfg': os.path.join(script_dir, "server_cfg"),
        'cfg_file': os.path.join(script_dir, f'server_cfg/server.cfg'),
        'logs': os.path.join(script_dir, "logs"),
        'local_mov_dir': f'{script_dir}/VODS/Movie_VOD',
        'master_mov_dir': f'{script_dir}/Movie_VOD',
        'local_tv_dir': f'{script_dir}/VODS/TV_VOD',
        'master_tv_dir': f'{script_dir}/TV_VOD',
        'master_unsorted': f'{script_dir}/Unsorted_VOD',
        'local_unsorted': f'{script_dir}/VODS/Unsorted_VOD',
        'm3u_dir': os.path.join(script_dir, "m3u"),
        'm3u_file_path': os.path.join(script_dir, "m3u_file.m3u"),
        'livetv_file': os.path.join(script_dir, "livetv.m3u"),
        'live_tv_dir': os.path.join(script_dir, f'VODS/Live_TV'),
        'tv_dir': os.path.join(script_dir, "TV_VOD"),
        'movies_dir': os.path.join(script_dir, "Movie_VOD"),
        'unsorted_dir': os.path.join(script_dir, "Unsorted_VOD"),
        'HOURS': os.getenv('HOURS', ""),
        'URLS': process_env_variable(os.getenv('M3U_URL', "")),
        'main_user': os.getenv('USER_NAME', ""),
        'main_pass': os.getenv('PASSWORD', ""),
        'SCRUB_HEADER': process_env_variable(os.getenv('SCRUB_HEADER', "")),
        'SCRUB_DEFAULTS': process_env_variable(os.getenv('SCRUB_DEFAULTS', "")),
        'REMOVE_TERMS': process_env_variable(os.getenv('REMOVE_TERMS', "")),
        'REMOVE_DEFAULTS': process_env_variable(os.getenv('REMOVE_DEFAULTS', "")),
        'REPLACE_TERMS': process_env_special(os.getenv('REPLACE_TERMS', "")),
        'REPLACE_DEFAULTS': process_env_special(os.getenv('REPLACE_DEFAULTS', "")),
        'CLEANERS': process_env_variable(os.getenv('CLEANERS', "")),
        'CLEANERS_DEFAULTS': process_env_variable(os.getenv('CLEANERS_DEFAULTS', "")),
        'UNSORTED': str_to_bool(os.getenv('UNSORTED', "")),
        'jellyfin_url': os.getenv('JELLYFIN_URL', ""),
        'epg_path': os.getenv('EPG_URL', ""),
        'server_name': os.getenv('SERVER_NAME', ""),
        'live_tv': str_to_bool(os.getenv('LIVE_TV', "")),
        'SERVER_CFG': str_to_bool(os.getenv('SERVER_SETUP', ""))

    }

    if args:
        # Return only specified variables
        return tuple(variables[arg] for arg in args if arg in variables)
    else:
        # Return all variables
        return variables


def create_vars():
    script_dir = os.path.dirname(os.path.dirname(__file__))
    variables = {
        'script_dir': os.path.dirname(os.path.dirname(__file__)),
        'server_cfg': os.path.join(script_dir, "server_cfg"),
        'cfg_file': os.path.join(script_dir, f'server_cfg/server.cfg'),
        'logs': os.path.join(script_dir, "logs"),
        'VODS': os.path.join(script_dir, "VODS"),
        'local_mov_dir': f'{script_dir}/VODS/Movie_VOD',
        'master_mov_dir': f'{script_dir}/Movie_VOD',
        'local_tv_dir': f'{script_dir}/VODS/TV_VOD',
        'master_tv_dir': f'{script_dir}/TV_VOD',
        'master_unsorted': f'{script_dir}/Unsorted_VOD',
        'local_unsorted': f'{script_dir}/VODS/Unsorted_VOD',
        'm3u_dir': os.path.join(script_dir, "m3u"),
        'm3u_file_path': os.path.join(script_dir, "m3u_file.m3u"),
        'livetv_file': os.path.join(script_dir, "livetv.m3u"),
        'live_tv_dir': os.path.join(script_dir, f'VODS/Live_TV'),
        'tv_dir': os.path.join(script_dir, "TV_VOD"),
        'movies_dir': os.path.join(script_dir, "Movie_VOD"),
        'unsorted_dir': os.path.join(script_dir, "Unsorted_VOD")

    }

    return variables


def cleaner_value(process_env_variable):

    cleaner_value = {
        'CLEANERS': process_env_variable(os.getenv('CLEANERS', "")),
        'CLEANERS_DEFAULTS': process_env_variable(os.getenv('CLEANERS_DEFAULTS', ""))
    }

    combined_cleaners = cleaner_value['CLEANERS'] + cleaner_value['CLEANERS_DEFAULTS']
    return combined_cleaners


def update_env_file(key, value):
    script_dir = os.path.dirname(os.path.dirname(__file__))
    cfg_file = os.path.join(script_dir, f'server_cfg/server.cfg')
    env_file = cfg_file

    # Read the existing .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()

    # Modify the lines to update or add the key-value pair
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break

    if not updated:
        lines.append(f"{key}={value}\n")

    # Write the updated .env file
    with open(env_file, 'w') as f:
        f.writelines(lines)


# update_env_file('SERVER_SETUP', 'True')


def print_config():
    variables = initialize_vars(process_env_variable, str_to_bool, process_env_special)
    print("Loaded Configuration:")

    for key, value in variables.items():
        print(f"{key}: {value}")

    if 'URLS' in variables:
        for url in variables['URLS']:
            print(f"Processing URL: {url}")


if __name__ == "__main__":
    print_config()
