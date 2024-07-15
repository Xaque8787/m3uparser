from parser.jellyfin_api.utility.server_init import setup_user, main_user


#================================
# Find setup User ID
#================================

def find_userID(client):
    try:
        # Send a request to the 'users' endpoint using the custom method
        response = client.jellyfin._get("Users")

        # Check if the request was successful (status code 200)
        if response:
            users = response
            for user in users:
                if user['Name'] == setup_user:
                    setup_user_id = user['Id']
                    print(f"User ID for '{setup_user}': {setup_user_id}")
                    return setup_user_id

            print(f"Username '{setup_user}' not found.")
        else:
            print("Failed to fetch users. Response is empty or None.")

    except Exception as e:
        print(f"Failed to fetch users: {e}")

    return None
    
#================================
# Find main User ID
#================================

def find_user_mainID(client):
    try:
        # Send a request to the 'users' endpoint using the custom method
        response = client.jellyfin._get("Users")

        # Check if the request was successful (status code 200)
        if response:
            users = response
            for user in users:
                if user['Name'] == main_user:
                    main_user_id = user['Id']
                    print(f"User ID for '{main_user}': {main_user_id}")
                    return main_user_id

            print(f"Username '{main_user}' not found.")
        else:
            print("Failed to fetch users. Response is empty or None.")

    except Exception as e:
        print(f"Failed to fetch users: {e}")

    return None
