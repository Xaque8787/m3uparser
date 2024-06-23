#!/bin/bash
#set -xe
# Write variables to remove_terms.txt
remove_file="./vars/terms.txt"
> "$remove_file"
REMOVE_TERMS_cleaned="${REMOVE_TERMS#\"}"
REMOVE_TERMS_cleaned="${REMOVE_TERMS_cleaned%\"}"
echo "$REMOVE_TERMS_cleaned" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' >> "$remove_file"

# Write variables to remove_terms.txt
remove_file2="./vars/removal.txt"
> "$remove_file2"
echo >> "$remove_file2"

# Write variables to headers.txt
header_file="./vars/header.txt"
> "$header_file"
SCRUB_HEADER_cleaned="${SCRUB_HEADER#\"}"
SCRUB_HEADER_cleaned="${SCRUB_HEADER_cleaned%\"}"
echo "$SCRUB_HEADER_cleaned" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' >> "$header_file"

# Write m3u_urls to urls.txt
url_file="./vars/urls.txt"
> "$url_file"
M3U_URL_cleaned="${M3U_URL#\"}"
M3U_URL_cleaned="${M3U_URL_cleaned%\"}"
echo "$M3U_URL_cleaned" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' >> "$url_file"

# Write apikey to jellyapi.txt
#api_file="./vars/jellyapi.txt"
#> "$api_file"
#JELLYFIN_API_cleaned="${JELLYFIN_API#\"}"
#JELLYFIN_API_cleaned="${JELLYFIN_API_cleaned%\"}"
#echo "$JELLYFIN_API_cleaned" > "$api_file"

# Clean the variable of leading and trailing double quotes
CLEANERS_cleaned="${CLEANERS#\"}"
CLEANERS_cleaned="${CLEANERS_cleaned%\"}"

# Remove any leading and trailing whitespace around each element
CLEANERS_cleaned=$(echo "$CLEANERS_cleaned" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr '\n' ',' | sed 's/,$//')

# Write variables to cleaners.txt
valid_cleaners=("series" "movies" "tv" "unsorted")
IFS=',' read -r -a cleaners_array <<< "$CLEANERS_cleaned"
declare -A present_cleaners
for cleaner in "${valid_cleaners[@]}"; do
    present_cleaners["$cleaner"]=false
done
for cleaner in "${cleaners_array[@]}"; do
    if [[ " ${valid_cleaners[*]} " =~ " $cleaner " ]]; then
        present_cleaners["$cleaner"]=true
    fi
done
cleaners_file="./vars/cleaners.txt"
> "$cleaners_file"
for cleaner in "${!present_cleaners[@]}"; do
    echo "$cleaner=${present_cleaners["$cleaner"]}" >> "$cleaners_file"
done
done

