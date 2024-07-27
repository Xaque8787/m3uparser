from parser.jellyfin_api.utility import *
from parser.jellyfin_api.user_clients import *
from parser.jellyfin_api.libraries import *
from parser.config.variables import *


def ezpztv_setup():
    try:
        print("Running server setup...")

        vars(configure_server, variables_all, 'jellyfin_url', 'setup_user', 'setup_pass')
        
        client = vars(create_client, variables_all, 'jellyfin_url', 'setup_user', 'setup_pass')
        
        add_media_libraries(client)
        
        vars(add_tuner_host, variables_all, client, 'jellyfin_url', 'live_tv')

        vars(add_epg_xml, variables_all, client, 'epg_path', 'jellyfin_url', 'live_tv')
        
        vars(create_main_user, variables_all, client, 'jellyfin_url', 'main_user', 'main_pass')
        
        main_user_id = vars(find_user_mainID, variables_all, client, 'main_user')
        
        vars(update_policy, variables_all, client, main_user_id, 'jellyfin_url')
        
        setup_user_id = vars(find_userID, variables_all, client, 'setup_user')
        
        main_client = vars(client_main_user, variables_all, 'jellyfin_url', 'main_user', 'main_pass')
        
        vars(library_options, variables_all, main_client, 'jellyfin_url')

        vars(library_refresh_disable, variables_all, main_client, 'jellyfin_url')
        
        vars(delete_user, variables_all, main_client, setup_user_id, 'jellyfin_url')
        
        vars(rebrand_server, variables_all, main_client, 'jellyfin_url', 'server_name')
        
        vars(upload_log, variables_all, main_client, 'log_file', 'jellyfin_url')

        print("Applying brand images...")
        vars(copy_png_files, variables_all, 'banner-light.png', 'images_file', 'banner_file')
        vars(copy_png_files, variables_all, 'banner-dark.png', 'images_file', 'banner_file')
        vars(copy_png_files, variables_all, 'icon-transparent.png', 'images_file', 'banner_file')
        vars(copy_png_files, variables_all, 'favicon.png', 'images_file', 'logo_file')
        vars(copy_png_files, variables_all, 'baba78f2a106d9baee83.png', 'images_file', 'logo_file')
        vars(copy_png_files, variables_all, 'bc8d51405ec040305a87.ico', 'images_file', 'logo_file')
        vars(copy_png_files, variables_all, 'favicon.ico', 'images_file', 'logo_file')

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    ezpztv_setup()
