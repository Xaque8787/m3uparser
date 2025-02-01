import os
import re
from dotenv import load_dotenv

# Process functions for environment variables
def process_env_variable(env_var_value):
    if isinstance(env_var_value, str):
        # Use regex to split on commas not preceded by a backslash
        items = re.split(r'(?<!\\),', env_var_value.strip('"'))

        # Remove any backslashes used for escaping commas and strip whitespace
        processed_value = [item.replace(r'\,', ',').strip() for item in items if item.strip()]

        return processed_value
    return env_var_value

# def process_env_variable(env_var_value):
#     if isinstance(env_var_value, str):
#         # print(f"Processing environment variable: {env_var_value}")
#         processed_value = [item.strip() for item in env_var_value.strip('"').split(',') if item.strip()]
#         # print(f"Processed environment variable: {processed_value}")
#         return processed_value
#     return env_var_value


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
        'local_mov_dir': f'/mnt/vods/Movie_VOD',
        'master_mov_dir': f'{root_dir}/Movie_VOD',
        'local_tv_dir': f'/mnt/vods/TV_VOD',
        'master_tv_dir': f'{root_dir}/TV_VOD',
        'master_unsorted': f'{root_dir}/Unsorted_VOD',
        'local_unsorted': f'{root_dir}/VODS/Unsorted_VOD',
        'm3u_dir': os.path.join(root_dir, "m3u"),
        'm3u_file_path': os.path.join(root_dir, "m3u_file.m3u"),
        'livetv_file': os.path.join(root_dir, "livetv.m3u"),
        'live_tv_dir': os.path.join(root_dir, f'/mnt/jellyfin/Live_TV'),
        'tv_dir': os.path.join(root_dir, "TV_VOD"),
        'movies_dir': os.path.join(root_dir, "Movie_VOD"),
        'unsorted_dir': os.path.join(root_dir, "Unsorted_VOD"),
        'HOURS': os.getenv('HOURS', ""),
        'URLS': process_env_variable(os.getenv('M3U_URL', "")),
        'main_user': os.getenv('USER_NAME', ""),
        'main_pass': os.getenv('PASSWORD', ""),
        'SCRUB_HEADER': process_env_variable(os.getenv('SCRUB_HEADER', "")),
        'SCRUB_DEFAULTS': process_env_variable(os.getenv('SCRUB_DEFAULTS', "")),
        'EXCLUDE_TERM': process_env_variable(os.getenv('EXCLUDE_TERMS', "")),
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
        'thread_user': os.getenv('TF_USER', ""),
        'thread_pass': os.getenv('TF_PASS', ""),
        'thread_url': os.getenv('TF_URL', ""),
        'host': os.getenv('TF_HOST', ""),
        'port': os.getenv('TF_PORT', ""),
        'application_version': os.getenv('APP_VERSION', ""),
        'lib_refresh': str_to_bool(os.getenv('REFRESH_LIB', "")),
        'remove_sync': str_to_bool(os.getenv('CLEAN_SYNC', "")),
        'url_m3u': os.getenv('M3U_URL', ""),
        'epg_xml': os.getenv('EPG_URL', ""),
        'apk_server': str_to_bool(os.getenv('APK', "")),
        'skip_header': str_to_bool(os.getenv('BYPASS_HEADER', "")),
        'SERVER_CFG': str_to_bool(os.getenv('SERVER_SETUP', "")),
        'APK_DLOAD': str_to_bool(os.getenv('APK_DLOAD', ""))

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
         jellyfin_url=None, thread_user=None, thread_pass=None, thread_url=None, tf_update=None,
         run_websocket_operations=None, run_reload_operations=None, apk_server=None, start_server=None, APK_DLOAD=None):
    try:

        if UNSORTED is True:
            print("Moving unsorted VOD")
            vars(sync_directories, variables_all, 'master_unsorted', 'local_unsorted', 'remove_sync')
        if live_tv is True:
            print("Moving livetv.m3u")
            vars(move_files, variables_all, 'livetv_file', 'live_tv_dir')
        if application_version in ["ezpztv", "threadfin"] and SERVER_CFG is True:
            wait_for_server(15)
            if application_version == "threadfin":
                print("Running Threadfin m3u/epg update")
                run_reload_operations()
            print("Running ezpztv start-up task")
            wait_for_server(15)
            ezpztv_task()
        if application_version in ["ezpztv", "threadfin"] and SERVER_CFG is False:
            wait_for_server(21)
            if application_version == "threadfin":
                print("Running Threadfin set-up and m3u/epg update")
                run_websocket_operations()
                run_reload_operations()
            ezpztv_setup()
            update_env_file('SERVER_SETUP', 'True')
        if application_version == "m3uparser" and APIKEY and jellyfin_url:
            if application_version == "threadfin":
                print("Running Threadfin m3u/epg update")
                run_reload_operations()
            print("Running ezpztv api start-up task")
            apikey_run()
        if application_version == "m3uparser" and thread_user and thread_pass:
            print("Running Threadfin m3u update")
            tf_update(thread_user, thread_pass, thread_url)
        if apk_server and APK_DLOAD is False:
            start_server()
            update_env_file('APK_DLOAD', 'True')
    except Exception as e:
        print(f"An error occurred: {e}")


# Debugging for variable values
jellyfin_variables = variables_all(process_env_variable, str_to_bool, process_env_special, 'URLS', 'SCRUB_HEADER', 'port', 'epg_path',
                                   'thread_url', 'm3u_file_path', 'remove_sync', 'main_user',
                                   'jellyfin_url', 'live_tv', 'UNSORTED', 'application_version', 'SERVER_CFG',
                                   'main_pass', 'log_file', 'script_dir', 'root_dir', 'REMOVE_TERMS', 'live_tv_dir',
                                   'livetv_file')
# jellyfin_url = jellyfin_variables['jellyfin_url']
# live_tv = f'{jellyfin_variables['port']}:{jellyfin_variables['host']}/{jellyfin_variables['live_tv_dir']}'
if __name__ == "__main__":
    print(jellyfin_variables)
    # print(live_tv)
