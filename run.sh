#!/bin/bash

# Path to the log file
log_file="/usr/src/app/VODS/log_file.log"
# Truncate the log file to ensure it's empty before appending new output
> "$log_file"
# Redirecting stdout and stderr of the script to the log file
exec &> "$log_file"


url_file="./vars/urls.txt"
# Loop through each URL in the file
while IFS= read -r vodurl; do
    # Check if URL is valid using wget --spider
    wget_output=$(wget --spider "$vodurl" 2>&1)

    # Check if the wget output contains "200 OK" and "Remote file exists."
    if [[ $wget_output == *"200 OK"* && $wget_output == *"Remote file exists."* ]]; then
        echo "URL is accessible and remote file exists. Proceeding with download."
        wget -P "./m3u/" "$vodurl"
    else
        echo "URL is not accessible or remote file does not exist: $vodurl"
    fi
done < "$url_file"

echo "All URLs processed."
# Directory containing the .m3u files
m3u_directory="/usr/src/app/m3u"
# Output file
output_file="/usr/src/app/m3u_file.m3u"
# Create the output file and add #EXTM3U at the beginning
echo "#EXTM3U" > "$output_file"
# Loop through each .m3u file in the specified directory
for m3u_file in "$m3u_directory"/*; do
    # Check if the file exists and is readable
    if [ -r "$m3u_file" ]; then
        # Append the contents of the file to the output file, skipping the first line
        tail -n +2 "$m3u_file" >> "$output_file"
    else
        echo "Cannot read $m3u_file"
    fi
done

echo "All files have been combined into $output_file"


# Run Python scripts
python3 "/usr/src/app/parser.py"
sleep 3
python3 "/usr/src/app/moviemover.py"
sleep 5
python3 "/usr/src/app/tvmover.py"
sleep 5

if [ "$UNSORTED" = "true" ]; then
    python3 "/usr/src/app/unsortedmover.py"
else
    rm -rf "/usr/src/app/Unsorted VOD"
fi

if [ "$LIVE_TV" = "true" ]; then
    cp -f ./livetv.m3u /usr/src/app/VODS/
fi

# Clean up
cd "/usr/src/app/"
rm -rf "/usr/src/app/Movie VOD"
rm -rf "/usr/src/app/TV VOD"
rm -rf "/usr/src/app/Unsorted VOD"
rm -f "/usr/src/app/m3u_file.m3u"
rm -f "/usr/src/app/livetv.m3u"
rm -rf /usr/src/app/m3u/*
sleep 5

exit 0

