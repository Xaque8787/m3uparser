import os
from dotenv import load_dotenv


# Process functions for environment variables
def process_env_variable(env_var_value):
    if isinstance(env_var_value, str):
        # print(f"Processing environment variable: {env_var_value}")
        processed_value = [item.strip() for item in env_var_value.strip('"').split(',') if item.strip()]
        # print(f"Processed environment variable: {processed_value}")
        return processed_value
    return env_var_value


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
def cleaner_value(process_env_variable):
    load_dotenv()

    cleaner_value = {
        'CLEANERS': process_env_variable(os.getenv('CLEANERS', "")),
        'CLEANERS_DEFAULTS': process_env_variable(os.getenv('CLEANERS_DEFAULTS', ""))
    }

    combined_cleaners = cleaner_value['CLEANERS'] + cleaner_value['CLEANERS_DEFAULTS']
    return combined_cleaners


def variables_all(process_env_variable, str_to_bool, process_env_special, *args):
    script_dir = os.path.dirname(os.path.dirname(__file__))
    root_dir = os.path.dirname(script_dir)
    cfg_file = os.path.join(root_dir, f'server_cfg/server.cfg')
    log_file = os.path.join(root_dir, f'logs/log_file.log')
    env_file = os.path.join(script_dir, 'config.env')
    load_dotenv(env_file)
    load_dotenv(cfg_file, override=True)
    variables = {
        'script_dir': os.path.dirname(os.path.dirname(__file__)),
        'root_dir': os.path.dirname(script_dir),
        'server_cfg': os.path.join(root_dir, "server_cfg"),
        'cfg_file': os.path.join(root_dir, f'server_cfg/server.cfg'),
        'logs': os.path.join(root_dir, "logs"),
        'log_file': f'{log_file}',
        'images_file': os.path.join(script_dir, f'assets'),
        'branding_file': os.path.join(root_dir, "branding"),
        'logo_file': os.path.join(root_dir, f'branding/web'),
        'banner_file': os.path.join(root_dir, f'branding/web/assets/img'),
        'local_mov_dir': f'{root_dir}/VODS/Movie_VOD',
        'master_mov_dir': f'{root_dir}/Movie_VOD',
        'local_tv_dir': f'{root_dir}/VODS/TV_VOD',
        'master_tv_dir': f'{root_dir}/TV_VOD',
        'master_unsorted': f'{root_dir}/Unsorted_VOD',
        'local_unsorted': f'{root_dir}/VODS/Unsorted_VOD',
        'm3u_dir': os.path.join(root_dir, "m3u"),
        'm3u_file_path': os.path.join(root_dir, "m3u_file.m3u"),
        'livetv_file': os.path.join(root_dir, "livetv.m3u"),
        'live_tv_dir': os.path.join(root_dir, f'VODS/Live_TV'),
        'tv_dir': os.path.join(root_dir, "TV_VOD"),
        'movies_dir': os.path.join(root_dir, "Movie_VOD"),
        'unsorted_dir': os.path.join(root_dir, "Unsorted_VOD"),
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
        'epg_path': process_env_variable(os.getenv('EPG_URL', "")),
        'server_name': os.getenv('SERVER_NAME', ""),
        'live_tv': str_to_bool(os.getenv('LIVE_TV', "")),
        'APIKEY': os.getenv('API_KEY', ""),
        'application_version': os.getenv('APP_VERSION', ""),
        'lib_refresh': str_to_bool(os.getenv('REFRESH_LIB', "")),
        'remove_sync': str_to_bool(os.getenv('CLEAN_SYNC', "")),
        'SERVER_CFG': str_to_bool(os.getenv('SERVER_SETUP', ""))

    }
    # if len(args) == 1:
    #     # Return the value of the single requested variable
    #     return variables.get(args[0], None)

    if args:
        # Return only specified variables
        return {arg: variables[arg] for arg in args if arg in variables}
    else:
        # Return all variables
        return variables

    # BELOW will return undefined KWARGS with value as the name. Somewhat undesirable in the current approach.
    # result = {}
    # for arg in args:
    #     if arg in variables:
    #         result[arg] = variables[arg]
    #     else:
    #         result[arg] = arg
    #
    # return result


def vars(func, vars_func, *args, **extra_kwargs):
    # Extract string arguments that may need processing
    string_args = [arg for arg in args if isinstance(arg, str)]

    # Fetch values from vars_func based on string_args
    all_vars = vars_func(process_env_variable, str_to_bool, process_env_special, *string_args)

    # Combine vars_func values and extra arguments
    combined_args = [
        all_vars.get(arg, arg) if isinstance(arg, str) else arg
        for arg in args
    ]

    # Process extra keyword arguments
    combined_kwargs = {
        key: all_vars.get(value, value) if isinstance(value, str) else value
        for key, value in extra_kwargs.items()
    }
    # print(f"Combined args: {combined_args}")
    # print(f"Combined kwargs: {combined_kwargs}")
    # Return the function call with combined arguments and keyword arguments
    result = func(*combined_args, **combined_kwargs)
    return result


def update_env_file(key, value):
    script_dir = os.path.dirname(os.path.dirname(__file__))
    root_dir = os.path.dirname(script_dir)
    cfg_file = os.path.join(root_dir, f'server_cfg/server.cfg')
    env_file = cfg_file
    # Read the existing config.env file
    with open(env_file, 'r') as f:
        lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break

    if not updated:
        lines.append(f"{key}={value}\n")

    # Write the updated config.env file
    with open(env_file, 'w') as f:
        f.writelines(lines)


def torf(move_files=None, live_tv=None, sync_directories=None, UNSORTED=None, SERVER_CFG=None, wait_for_server=None,
         ezpztv_task=None, ezpztv_setup=None, application_version=None, APIKEY=None, apikey_run=None,
         jellyfin_url=None):
    try:

        if UNSORTED is True:
            print("Moving unsorted VOD")
            vars(sync_directories, variables_all, 'master_unsorted', 'local_unsorted', 'remove_sync')
        if live_tv is True:
            print("Moving livetv.m3u")
            vars(move_files, variables_all, 'livetv_file', 'live_tv_dir')
        if application_version == "ezpztv" and SERVER_CFG is True:
            print("Running ezpztv start-up task")
            wait_for_server(12)
            ezpztv_task()
        if application_version == "ezpztv" and SERVER_CFG is False:
            wait_for_server(21)
            ezpztv_setup()
            update_env_file('SERVER_SETUP', 'True')
        if application_version == "m3uparser" and APIKEY and jellyfin_url:
            print("Running ezpztv api start-up task")
            apikey_run()
    except Exception as e:
        print(f"An error occurred: {e}")


# Debugging for variable values
jellyfin_variables = variables_all(process_env_variable, str_to_bool, process_env_special, 'remove_sync', 'main_user',
                                   'jellyfin_url', 'live_tv', 'UNSORTED', 'application_version', 'SERVER_CFG',
                                   'main_pass', 'log_file', 'script_dir', 'root_dir', 'images_file', 'logo_file',
                                   'banner_file', 'lib_refresh', 'REMOVE_TERMS')
jellyfin_url = jellyfin_variables['jellyfin_url']
live_tv = jellyfin_variables['live_tv']
if __name__ == "__main__":
    print(jellyfin_variables)
