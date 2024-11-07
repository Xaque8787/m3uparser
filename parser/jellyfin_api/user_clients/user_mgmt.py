from jellyfin_apiclient_python import JellyfinClient
import json

#================================
# Create main Jellyfin user
#================================


def create_main_user(client, jellyfin_url, main_user, main_pass):

    try:
    # Prepare headers for the request
        headers = client.jellyfin.get_default_headers()
        headers.update({
            "Content-Type": "application/json"
        })

        # Create a new user with elevated privileges
        response = client.jellyfin.send_request(
            jellyfin_url,
            "Users/New",
            method="post",
            headers=headers,
            data=json.dumps({
                "Name": main_user,
                "Password": main_pass
            })
        )

        if response.status_code == 200:
            print("New user created successfully.")
        else:
            print(f"Failed to create new user. Status Code: {response.status_code}, Response: {response.content}")

    except Exception as e:
        print(f"Failed to create or login to server: {e}")

    return None

#================================
# Create main user client for API
#================================


def client_main_user(jellyfin_url, main_user, main_pass):

    # Initialize the client
    main_client = JellyfinClient()
    main_client.config.app(
        name='ezpztv',
        version='21.12',
        device_name='device',
        device_id='211290125'
    )
    print("Authenticated as main user")
    main_client.config.data["auth.ssl"] = True
    # Authenticate to the server with username and password
    main_client.auth.connect_to_address(jellyfin_url)
    main_client.auth.login(jellyfin_url, main_user, main_pass)
    
    # Generate a token and authenticate with elevated privileges
    credentials = main_client.auth.credentials.get_credentials()
    server = credentials["Servers"][0]
    server["username"] = main_user

    main_client.authenticate({"Servers": [server]}, discover=False)
    print("Authenticated as main user")
    return main_client

#================================
# Create setup client for API
#================================


def create_client(jellyfin_url, setup_user, setup_pass):
    client = JellyfinClient()
    client.config.app(
        name='ezpztv',
        version='21.12',
        device_name='device',
        device_id='211290125'
    )
    client.config.data["auth.ssl"] = True

    # Authenticate to the server with username and password
    client.auth.connect_to_address(jellyfin_url)
    client.auth.login(jellyfin_url, setup_user, setup_pass)

    # Generate a token and authenticate with elevated privileges
    credentials = client.auth.credentials.get_credentials()
    server = credentials["Servers"][0]
    server["username"] = setup_user

    client.authenticate({"Servers": [server]}, discover=False)
    
    return client

#================================
# Deletes setup user from server
#================================


def delete_user(main_client, user_id, jellyfin_url):
    try:
        # Prepare headers for the request
        headers = main_client.jellyfin.get_default_headers()
        headers.update({
            "Content-Type": "application/json"
        })

        # Send the request to delete the user
        delete_response = main_client.jellyfin.send_request(
            jellyfin_url,
            f"Users/{user_id}",
            method="delete",
            headers=headers
        )

        if delete_response.status_code == 204:
            print("User deleted successfully.")
        else:
            print(f"Failed to delete user. Status Code: {delete_response.status_code},"
                  f" Response: {delete_response.content}")

    except Exception as e:
        print(f"Failed to delete user: {e}")

    return None

#================================
# Update main user settings
#================================

def update_policy(client, main_user_id, jellyfin_url):
    try:
        # Prepare headers for the request
        headers = client.jellyfin.get_default_headers()
        headers.update({
            "Content-Type": "application/json"
        })

        # Define the user policy values to update
        user_policy = {
            "IsAdministrator": True,
            "EnableAudioPlaybackTranscoding": True,
            "EnableVideoPlaybackTranscoding": True,
            "EnableSubtitleManagement": True,
            "EnableContentDeletion": True,
            "AuthenticationProviderId": "Jellyfin.Server.Implementations.Users.DefaultAuthenticationProvider",
            "PasswordResetProviderId": "Jellyfin.Server.Implementations.Users.DefaultPasswordResetProvider"
        }

        # Send the updated user policy to the server
        update_response = client.jellyfin.send_request(
            jellyfin_url,
            f"Users/{main_user_id}/Policy",
            method="post",
            headers=headers,
            data=json.dumps(user_policy)
        )

        if update_response.status_code == 204:
            print("User policy updated successfully.")
        else:
            print(f"Failed to update user policy. Status Code: {update_response.status_code},"
                  f" Response: {update_response.content}")

    except Exception as e:
        print(f"Failed to update user policy: {e}")


# if __name__ == "__main__":
