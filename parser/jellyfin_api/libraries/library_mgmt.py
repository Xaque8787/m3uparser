import json

# ================================
# Add TV and Movie libraries
# ================================


def add_media_libraries(client):
    libraries = [
        {'name': 'Movies', 'collectionType': 'movies', 'paths': ['/data/movies']},
        {'name': 'TV', 'collectionType': 'tvshows', 'paths': ['/data/tvshows']}
    ]
    for lib in libraries:
        try:
            print(f"Adding media library: {lib['name']}, Type: {lib['collectionType']}, Paths: {lib['paths']}")
            client.jellyfin.add_media_library(
                name=lib['name'], 
                collectionType=lib['collectionType'], 
                paths=lib['paths'], 
                refreshLibrary=True
            )
            print(f"Successfully added library: {lib['name']}")
        except Exception as e:
            print(f"Failed to add library: {lib['name']}. Error: {e}")


# ================================
# GET library ID values
# ================================


def library_options(main_client, jellyfin_url):
    headers = main_client.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "application/json"
    })
    
    try:
        response = main_client.jellyfin.send_request(
            jellyfin_url,
            "Library/VirtualFolders",
            method="get",
            headers=headers
        )

        if response.status_code == 200:
            print("Library options IDs was successful.")
            data = response.json()
            for library in data:
                # Extract relevant data
                name = library.get('Name')
                item_id = library.get('ItemId')
                
                # Create variables dynamically
                globals()[f"{name}_ID"] = item_id
                
                # Optionally print for verification
                print(f"{name}_ID = {item_id}")
                
                # Call the post function with each library ID
                library_options_post(item_id, main_client, jellyfin_url)
                
        else:
            print(f"Failed to retrieve library options. Status Code: {response.status_code},"
                  f" Response: {response.content}")

    except Exception as e:
        print(f"Failed to retrieve virtual folder: {e}")

# ================================
# POST library option values
# ================================


def library_options_post(library_id, main_client, jellyfin_url):
    headers = main_client.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "application/json"
    })
    
    lib_opt = {
        "Id": f"{library_id}",
        "LibraryOptions": {
            "EnableRealtimeMonitor": True
        }
    }

    try:
        response = main_client.jellyfin.send_request(
            jellyfin_url,
            "Library/VirtualFolders/LibraryOptions",
            method="post",
            headers=headers,
            data=json.dumps(lib_opt)
        )

        if response.status_code == 204:
            print(f"Library options for ID {library_id} were successfully updated.")
            # print(json.dumps(response.json(), indent=4))
        else:
            print(f"Failed to update library options for ID {library_id}. Status Code: {response.status_code},"
                  f" Response: {response.content}")

    except Exception as e:
        print(f"Failed to update library options: {e}")

# ================================
# Add TV Tuner (m3u file or url)
# ================================


def add_tuner_host(client, jellyfin_url, live_tv):
    if live_tv:
        tuner_host_data = {
            "Id": "211290125",
            "Url": "/data/livetv.m3u",
            "Type": "M3U",
            "FriendlyName": "LiveTV",
            "ImportFavoritesOnly": False,
            "AllowHWTranscoding": True,
            "EnableStreamLooping": False,
            "Source": "File",
            "TunerCount": 1,
            "UserAgent": "your-user-agent",
            "IgnoreDts": True
        }

        headers = client.jellyfin.get_default_headers()
        headers.update({
            "Content-Type": "application/json"
        })

        try:
            response = client.jellyfin.send_request(
                jellyfin_url,
                "LiveTv/TunerHosts",
                method="post",
                headers=headers,
                data=json.dumps(tuner_host_data)
            )

            if response.status_code == 200:
                print("Tuner Host added successfully.")
            else:
                print(f"Failed to add Tuner Host. Status Code: {response.status_code}, Response: {response.content}")

        except Exception as e:
            print(f"Failed to add Tuner Host: {e}")
    else:
        print(f"Failed to add Tuner Host")


# ====================================
# Add EPG to Tuners (m3u file or url)
# ====================================


def add_epg_xml(client, epg_path, jellyfin_url, live_tv):
    if live_tv:
        # Ensure epg_path is a list, even if it's a single URL
        if isinstance(epg_path, str):
            epg_urls = [epg_path]
        else:
            epg_urls = epg_path

        headers = client.jellyfin.get_default_headers()
        headers.update({
            "Content-Type": "application/json"
        })

        for url in epg_urls:
            epg_data = {
                "Type": "XMLTV",
                "Path": url,
                "EnableAllTuners": True
            }

            try:
                response = client.jellyfin.send_request(
                    jellyfin_url,
                    "LiveTv/ListingProviders",
                    method="post",
                    headers=headers,
                    data=json.dumps(epg_data)
                )

                if response.status_code == 200:
                    print(f"EPG XML for {url} added successfully.")
                else:
                    print(f"Failed to add EPG XML for {url}. Status Code: {response.status_code}")
            except Exception as e:
                print(f"Exception occurred while adding EPG XML for {url}: {e}")
    else:
        print("Live TV is not enabled.")

# ====================================
# Disable scheduled library refresh
# ====================================


def library_refresh_disable(main_client, jellyfin_url):
    task_id = "7738148ffcd07979c7ceb148e06b3aed"

    task_data = []

    headers = main_client.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "application/json"
    })

    try:
        response = main_client.jellyfin.send_request(
            jellyfin_url,
            f"/ScheduledTasks/{task_id}/Triggers",
            method="post",
            headers=headers,
            data=json.dumps(task_data)
        )

        if response.status_code == 204:
            print("Library refresh task has been removed.")
        else:
            print(f"Failed to update task options. Status Code: {response.status_code}, Response: {response.content}")

    except Exception as e:
        print(f"Failed to remove refresh task options: {e}")


# ====================================
# Run Library refresh REFRESH_LIB=true
# ====================================


def run_library_task(main_client, jellyfin_url, lib_refresh):
    if lib_refresh:
        try:
            headers = main_client.jellyfin.get_default_headers()
            # Send POST request to the specified endpoint
            response = main_client.jellyfin.send_request(
                jellyfin_url,
                "/Library/Refresh",
                method="post",
                headers=headers
            )

            if response.status_code == 204:
                print("Library refresh task started successfully.")
            elif response.status_code == 401:
                print("Library refresh task failed")
            else:
                print(f"Failed to start Library refresh task. Status Code: {response.status_code},"
                      f" Response: {response.content}")

        except Exception as e:
            print(f"Failed to start Library refresh task: {e}")
    else:
        print(f"Library refresh is set to false, set REFRESH_LIB=true in compose file to enable")

# ====================================
# Run TV guide refresh
# ====================================


def run_scheduled_task(main_client, jellyfin_url, live_tv):
    # Use built-in method to get default headers
    headers = main_client.jellyfin.get_default_headers()
    if live_tv:
        try:
            # Send POST request to the specified endpoint
            response = main_client.jellyfin.send_request(
                jellyfin_url,
                "ScheduledTasks/Running/bea9b218c97bbf98c5dc1303bdb9a0ca",
                method="post",
                headers=headers
            )

            if response.status_code == 204:
                print("Scheduled task started successfully.")
            else:
                print(f"Failed to start scheduled task. Status Code: {response.status_code},"
                      f" Response: {response.content}")

        except Exception as e:
            print(f"Failed to start scheduled task: {e}")
    else:
        print("Live TV is not enabled.")

# ====================================
# Disable scheduled subtitle download task
# ====================================


def sub_dload_disable(main_client, jellyfin_url):
    task_id = "2c66a88bca43e565d7f8099f825478f1"

    task_data = []

    headers = main_client.jellyfin.get_default_headers()
    headers.update({
        "Content-Type": "application/json"
    })

    try:
        response = main_client.jellyfin.send_request(
            jellyfin_url,
            f"/ScheduledTasks/{task_id}/Triggers",
            method="post",
            headers=headers,
            data=json.dumps(task_data)
        )

        if response.status_code == 204:
            print("Download Subtitle task has been removed.")
        else:
            print(f"Failed to update task options. Status Code: {response.status_code}, Response: {response.content}")

    except Exception as e:
        print(f"Failed to remove subtitle task options: {e}")



# ================================
# GET schedule task values DEPRECATED
# ================================

# def scheduled_task_values(main_client):
#     headers = main_client.jellyfin.get_default_headers()
#     headers.update({
#         "Content-Type": "application/json"
#     })
#
#     try:
#         response = main_client.jellyfin.send_request(
#             jellyfin_url,
#             "ScheduledTasks/7738148ffcd07979c7ceb148e06b3aed",
#             method="get",
#             headers=headers
#         )
#
#         if response.status_code == 200:
#             print("Library options IDs was successful.")
#             data = response.json()
#
#             # Extract the LastExecutionResult dictionary
#             sched_task_lib = data.get("LastExecutionResult")
#
#             # Optionally print for verification
#             print("Scheduled Task Library:", sched_task_lib)
#
#             # Check if Status is "Completed" and both StartTimeUtc and EndTimeUtc are non-null
#             if (sched_task_lib is not None and
#                 sched_task_lib.get("Status") == "Completed" and
#                 sched_task_lib.get("StartTimeUtc") and
#                 sched_task_lib.get("EndTimeUtc")):
#
#                 library_refresh_disable(main_client)

# ====================================
# Add EPG to Tuners (m3u file or url) - single url, deprecated.
# ====================================

# def add_epg_xml_single(client):
#
#     epg_data = {
#         "Type": "XMLTV",
#         "Path": epg_path,
#         "EnableAllTuners": True
#     }
#
#     headers = client.jellyfin.get_default_headers()
#     headers.update({
#         "Content-Type": "application/json"
#     })
#
#     try:
#         response = client.jellyfin.send_request(
#             jellyfin_url,
#             "LiveTv/ListingProviders",
#             method="post",
#             headers=headers,
#             data=json.dumps(epg_data)
#         )
#
#         if response.status_code == 200:
#             print("EPG XML added successfully.")
#         else:
#             print(f"Failed to add EPG XML. Status Code: {response.status_code}, Response: {response.content}")
#
#     except Exception as e:
#         print(f"Failed to add EPG XML: {e}")

#
#     except Exception as e:
#         print(f"An error occurred: {e}")
