from parser.jellyfin_api.utility import server_init, logs, find_values
from parser.jellyfin_api.user_clients import user_mgmt
from parser.jellyfin_api.libraries import library_mgmt
from parser.jellyfin_api.utility.server_init import live_tv, log_file_path


def ezpztv():
    try:
        
        server_init.configure_server()
        
        client = user_mgmt.create_client()
        
        library_mgmt.add_media_libraries(client)
        
        if live_tv:
            library_mgmt.add_tuner_host(client)
            library_mgmt.add_epg_xml(client)
        
        user_mgmt.create_main_user(client)
        
        main_user_id = find_values.find_user_mainID(client)
        
        user_mgmt.update_policy(client, main_user_id)
        
        setup_user_id = find_values.find_userID(client)
        
        main_client = user_mgmt.client_main_user()
        
        library_mgmt.library_options(main_client)
        
        user_mgmt.delete_user(main_client, setup_user_id)
        
        server_init.rebrand_server(main_client)
        
        logs.upload_log(log_file_path, main_client)
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    ezpztv()
