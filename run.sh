#!/bin/bash

# Path to the log file
log_file="/usr/src/app/log_file.log"

# Truncate the log file to ensure it's empty before appending new output
> "$log_file"

# Redirecting stdout and stderr of the script to the log file
exec &> "$log_file"


# Save the VOD URL to a configuration file
echo "$VOD_URL" > /usr/src/app/vodurl.cfg
sleep 3

# Read the destination folder and VOD URL from configuration files
read -r destination < /usr/src/app/destination.cfg
sleep 3
read -r vodurl < /usr/src/app/vodurl.cfg
sleep 3

# Use wget to check URL availability
wget_output=$(wget --spider "$vodurl" 2>&1)

# Check if the wget output contains "200 OK" and "Remote file exists."
if [[ $wget_output == *"200 OK"* && $wget_output == *"Remote file exists."* ]]; then
    echo "URL is accessible and remote file exists. Proceeding with download."
    wget -O "/usr/src/app/m3u_file.m3u" $vodurl
    
    # Run Python scripts
    python3 "/usr/src/app/parser.py"
    sleep 3
    python3 "/usr/src/app/moviemover.py"
    sleep 5
    python3 "/usr/src/app/tvmover.py"
    sleep 5

    # Clean up
    cd "/usr/src/app/"
    rm -rf "/usr/src/app/Movie VOD"
    rm -rf "/usr/src/app/TV VOD"
    rm -r "/usr/src/app/m3u_file.m3u"
else
    echo "URL is not accessible or remote file does not exist. Exiting script."
    exit 1
fi

# Copy the log file to the desired directory (/usr/src/app/VODS)
cp -f "/usr/src/app/log_file.log" "/usr/src/app/VODS/log_file.log"

sleep 5

exit 0

