from processors import *
from utils import *
from config import *


def main():
    try:
        # Initialize folders
        dirmake(create_vars)
        # Initialize variables
        init_var = initialize_vars(process_env_variable, str_to_bool, process_env_special)
        # Set up logging
        setup_logging(f'{init_var['logs']}/log_file.log')
        # Download & concatenate all m3u urls
        prepare_m3us(*vars_position(process_env_variable, str_to_bool, process_env_special, 'URLS', 'm3u_dir',
                                    'm3u_file_path'))
        # Parse the m3u file and get a list of dictionaries containing key-value pairs
        entries, errors = parse_m3u_file(init_var['m3u_file_path'], clean_group_title, process_value,
                                         *vars_position(process_env_variable, str_to_bool, process_env_special,
                                                        'REPLACE_TERMS', 'REPLACE_DEFAULTS', 'SCRUB_HEADER',
                                                        'SCRUB_DEFAULTS', 'REMOVE_TERMS', 'REMOVE_DEFAULTS'))
        # Process each entry dictionary and track created .strm files
        proc_entries(entries, errors, *vars_position(process_env_variable, str_to_bool, process_env_special,
                                                     'tv_dir', 'movies_dir', 'unsorted_dir'))
        # Extract live TV entries and process them separately
        live_tv_entries = [entry for entry in entries if entry.get('livetv')]
        process_live_tv_entries(live_tv_entries, *vars_position(process_env_variable, str_to_bool, process_env_special,
                                                                'livetv_file'))
        # Sync items from VOD m3us to local directories
        sync_directories(*vars_position(process_env_variable, str_to_bool, process_env_special,
                                        'movies_dir', 'local_mov_dir'))
        sync_directories(*vars_position(process_env_variable, str_to_bool, process_env_special,
                                        'tv_dir', 'local_tv_dir'))
        if init_var['UNSORTED'] is True:
            sync_directories(*vars_position(process_env_variable, str_to_bool, process_env_special, 'master_unsorted',
                                            'local_unsorted'))
        # Move livetv.m3u
        if init_var['live_tv'] is True:
            move_files(*vars_position(process_env_variable, str_to_bool, process_env_special, 'livetv_file', 'live_tv_dir'))
        # Count .strm files and live TV channels
        [livetv_channels_count, movie_strm_count, tv_strm_count, unsorted_strm_count] =\
            count_emup(live_tv_entries, *vars_position(process_env_variable, str_to_bool, process_env_special,
                                                       'tv_dir', 'movies_dir', 'unsorted_dir'))
        # Clean-up files and folders
        clean_up()
        # Output errors if any
        errz(errors)
        # Output results
        final_output(errors, livetv_channels_count, movie_strm_count, tv_strm_count, unsorted_strm_count)
        # Wait interval time to re-run script
        wait_time = int(init_var['HOURS']) * 3600
        run_timer(main, wait_time)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
