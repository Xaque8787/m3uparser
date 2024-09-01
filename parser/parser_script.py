from processors import *
from utils import *
from config import *
from jellyfin_api import *
from threadfin import *
from server_apk import *


def main():
    try:
        # Initialize folders
        vars(dirmake, variables_all, 'server_cfg', 'cfg_file', 'logs', 'm3u_dir', 'livetv_file', 'live_tv_dir',
             'tv_dir', 'movies_dir', 'unsorted_dir', 'log_file', 'branding_file', 'local_tv_dir', 'local_mov_dir',
             'local_unsorted')
        # Set up logging
        vars(setup_logging, variables_all, 'log_file')
        # Download & concatenate all m3u urls
        vars(prepare_m3us, variables_all, 'URLS', 'm3u_dir', 'm3u_file_path')
        # Parse the m3u file and get a list of dictionaries containing key-value pairs
        entries, errors = vars(parse_m3u_file, variables_all, 'm3u_file_path', clean_group_title, process_value,
                               'REPLACE_TERMS', 'REPLACE_DEFAULTS', 'SCRUB_HEADER', 'SCRUB_DEFAULTS', 'REMOVE_TERMS',
                               'REMOVE_DEFAULTS')
        # Process each entry dictionary and track created .strm files
        vars(proc_entries, variables_all, entries, errors, 'tv_dir', 'movies_dir', 'unsorted_dir')
        # Extract live TV entries and process them separately
        live_tv_entries = [entry for entry in entries if entry.get('livetv')]
        vars(process_live_tv_entries, variables_all, live_tv_entries, 'livetv_file')
        # Sync items from VOD m3us to local directories & Move livetv.m3u
        vars(sync_directories, variables_all, 'movies_dir', 'local_mov_dir', 'remove_sync')
        vars(sync_directories, variables_all, 'tv_dir', 'local_tv_dir', 'remove_sync')
        vars(torf, variables_all, move_files=move_files, live_tv='live_tv', sync_directories=sync_directories,
             UNSORTED='UNSORTED')
        # Count .strm files and live TV channels
        [livetv_channels_count, movie_strm_count, tv_strm_count, unsorted_strm_count] = vars(count_emup, variables_all,
                                                                                             live_tv_entries,
                                                                                             'tv_dir', 'movies_dir',
                                                                                             'unsorted_dir')
        # Clean-up files and folders
        vars(clean_up, variables_all, 'm3u_dir', 'm3u_file_path', 'master_mov_dir', 'master_tv_dir',
             'master_unsorted', 'live_tv', 'livetv_file', 'live_tv_dir', 'UNSORTED', 'local_unsorted')
        # Output errors if any
        errz(errors)
        # Output results
        final_output(errors, livetv_channels_count, movie_strm_count, tv_strm_count, unsorted_strm_count)
        # Run Jellyfin server set-up and/or ezpztv_task
        vars(torf, variables_all, SERVER_CFG='SERVER_CFG', wait_for_server=wait_for_server,  ezpztv_task=ezpztv_task,
             ezpztv_setup=ezpztv_setup, application_version='application_version', APIKEY='APIKEY', tf_update=tf_update,
             jellyfin_url='jellyfin_url', thread_user='thread_user', thread_pass='thread_pass', thread_url='thread_url',
             apikey_run=apikey_run, run_websocket_operations=run_websocket_operations,
             run_reload_operations=run_reload_operations, apk_server='apk_server',
             start_server=start_server, APK_DLOAD='APK_DLOAD')
        # Wait interval time to re-run script
        vars(run_timer, variables_all, main, 'HOURS')

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
