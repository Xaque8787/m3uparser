![m3uparser](./parser/assets/other_img/logo.png)

# m3u|>arser

m3u|>arser will parse your m3u urls and make a .strm library.

Docker Compose Example

```
services:
  m3uparser:
    container_name: m3uparser
    image: xaque87/m3uparser:latest
    environment:
      - PUID=1000 # Defaults 1000 if blank.
      - PGID=1000 # Defaults 1000 if blank.
      - M3U_URL= # "https://m3u_URL1.com, https://m3u_URL2.com, etc..."
      - HOURS=12 # update interval, setting this optional, default 12hrs.
      - SCRUB_HEADER= # Optional, add more/different scrub values, does not override the defaults
      - REMOVE_TERMS= # Optional, add more/different remove term values, does not override the defaults
      - REPLACE_TERMS # Optional, add more/different replace values, does not override the defaults
      - CLEANERS= # Optional, add more/different cleaner values, does not override the defaults
      - CLEAN_SYNC= # If set to true will remove titles from VOD folders that are not present in m3u files, Defaults to false if blank.
      - LIVE_TV= # Default is true, true will make a combined livetv.m3u from all live tv streams found in m3u files. Will be placed in /VODS/Live_TV 
      - UNSORTED= # Default is false, true will put at /VODS/Unsorted_VOD
      - JELLYFIN_URL= # Requires a Jellyfin server to be running. http://<jfin_url:8096>
      - API_KEY= # Generate API key on server and enter it here. Requires a Jellyfin server to be running.
      -TF_HOST= # IP address used for Threadfin, example 127.0.0.1
      -TF_PORT= # Port used for Threadfin, example 34400
      -TF_USER= # Username being used for Threadfin
      -TF_PASS= # Password for Threadfin
      - REFRESH_LIB= # Requires a Jellyfin server to be running. Will refresh libraries after each parsing.

    volumes:
      - /path/to/your/media/library:/usr/src/app/VODS
      - /path/to/your/media/library:/usr/src/app/logs/
```

| ENV VARIABLE  | VALUES                                              | DESCRIPTION                                                                                                   | EXAMPLE                                      | DEFAULT VALUES                      |
| ------------- |:---------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------:|:--------------------------------------------:|:-----------------------------------:|
| M3U_URL       | any url(s), in quotes, and seperated with a comma , | Include all URLs you want to be parsed                                                                        | "https://m3u_URL1.com, https://m3u_URL2.com" | n/a                                 |
| BYPASS_HEADER | true/false                                          | Bypass checking url header for content-type and content-disposition.                                          | False                                        | False                               |
| HOURS         | numeric value                                       | Number representing the interval you want to update from m3u urls                                             | 12                                           | 8                                   |
| SCRUB_HEADER  | any text, in quotes, and seperated with a comma ,   | Removes value and preceding text from begining of group-title line                                            | "HD :"                                       | "HD :, SD :"                        |
| REMOVE_TERMS  | any text, in quotes, and seperated with a comma ,   | Removes value(s) set from file and directory names                                                            | "x264, 720p"                                 | "720p, WEB, h264, H264, HDTV, x264" |
| REPLACE_TERMS | "term-to-replace=replace-value"                     | Replaces one value with another. Separate terms with an = and term on left is replaced with term to the right | "replace-this=with-this"                     | "1/2=\u00BD, /=-"                   |
| CLEANERS      | series,movie,tv,unsorted                            | Type of stream to apply REMOVE_TERMS value to                                                                 | tv, movies                                   | tv                                  |
| REFRESH_LIB   | true/false                                          | Refresh Jellyfin libraries after parsing                                                                      | false                                        | false                               |
| CLEAN_SYNC    | true/false                                          | Will remove titles from VOD folders that are not present in m3u.                                              | false                                        | false                               |
| LIVE_TV       | true/false                                          | Parse live tv streams in m3u urls and creates a single livetv.m3u                                             | true/false                                   | true                                |
| UNSORTED      | true/false                                          | Creates a VOD folder for undefined streams, either misspelled or poorly labeled streams                       | true/false                                   | false                               |

## Instalation Process

```
mkdir m3uparser
cd m3uparser
curl -o docker-compose.yaml https://raw.githubusercontent.com/Xaque8787/m3uparser/main/m3uparser/docker-compose.yaml
curl -o ezpztv.env https://raw.githubusercontent.com/Xaque8787/m3uparser/main/m3uparser/m3uparser.env
```

Then edit the m3uparser.env file with your credentials and desired values.

Then run:

```
docker compose up -d
```

## Basic Information

### Expanding default values

**Add more values to the environment variables in the compose file to extend the defaults.**

### How it works

The parser uses the `group-title` value in the `#EXTINF` line of m3u files to structure the file and folder hierarchy. There are five stream types:

- **series**: Shows with season/episode values.
- **tv**: Shows with 'aired on date', such as talk shows with guest stars.
- **movies**: Movies with release years.
- **live-tv**: Live TV streams.
- **unsorted**: Streams that do not fit into the above categories.

Key=Value pairs are made from each item in the EXTINF line. The values are then used to determine stream type, extract relavent information, and finally clean out unwanted values to then make the end resulting .strm libraries.

## Examples and Explanations

### SCRUB_HEADER

Example: `SCRUB_HEADER="HD :, SD :"`. This removes these values, if they exist, and any preceding text from the `group-title` line. So a line like this, `group-title="Movie VOD",HD : The Fall Guy 2024` will become `group-title= The Fall Guy 2024`. Ensure spaces are included where needed. Add multiple values to `SCRUB_HEADER=`, separated by commas, in a single set of quotes.

Default is set to: `SCRUB_HEADER="HD :, SD :"`

### REMOVE_TERMS & CLEANERS

`REMOVE_TERMS` removes specified terms, and any attatched text, from titles. For instance, `REMOVE_TERMS="x264"`, would remove the entire string `x264-somegarbge`. This setting is case-sensitive and should have multiple values separated by commas, in a single set of quotes. i.e `REMOVE_TERMS="x264, h264, X264"`

Default is set to: `"720p, WEB, h264, H264, HDTV, x264"`

The `CLEANERS` variable defines which stream types `REMOVE_TERMS` applies to. For example, `CLEANERS=series,tv` applies `REMOVE_TERMS` to series and TV shows.

Default is set to: `tv`

### REPLACE_TERMS

Add more replacements to `REPLACE_TERMS` in the format `"replace=value"`. For example: `REPLACE_TERMS="replace-this=with-this, dontwant=wantinstead"`. This replaces specified terms in all streams, except live TV.

Default is set to: `"1/2=\u00BD, /=-"`

### JELLYFIN INTEGRATION;   JELLYFIN_URL, API_KEY, REFRESH_LIB

To utilize the Jellyfin integration, you must have a Jellyfin server accessible if you supplied the compose file with the `API_KEY` and `JELLYFIN_URL` env variable. If you supply a address to your working server, and an api key you generated on that server; then when this script is ran it will refresh your library if `REFRESH_LIB=true` to add new titles that are in m3u urls, if `CLEAN_SYNC=true` it will also then remove any titles not found in the m3u urls but are in your VOD libraries. If you have `LIVE_TV=true`, then it will also refresh your tv guide.

**`JELLYFIN_URL`** should include http:// or https:// (DO NOT SURROUND WITH "")
Logs will now be uploaded to the server as well.
**`API_KEY`** Generate on server. Dashboard > Api Key > Add
**`REFRESH_LIB`** True or false, depending on your preference.

If you do not have a Jellyfin server set up, but would like a easy way to get one set up, checkout the branch of this repo for an automated setup https://github.com/Xaque8787/m3uparser/tree/ezpztv

### THREADFIN INTEGRATION;   TF_HOST, TF_PORT, TF_USER, TF_PASS

If you have Threadfin setup and want to refresh the m3u/xmltv data when the script is run/re run, then supply the ip:port username and password to the appropriate env variables.

### BYPASS_HEADER

Setting this to true will have the script download the m3u urls regardless if it is available from provider or not. It will still check for 200 response from url, but will not check for content-type or content-disposition from the header response. These two checks are useful for ensuring the m3u file downloaded is actually available from the provider. In some cases if your provider is "down", you still may get a 200ok response from their server, but the m3u file that will be downloaded will be empty, resulting in a failed parsing. There are cases where the provider does not have a content-disposition entry in their url header response, so setting this env variable to false will bypass this check and download the m3u file regardless. 

### CLEAN_SYNC

If this is set to true, then every time a parsing of m3u urls is complete, it will add new content from the m3u urls to your VOD libraries, and any content in your VOD libraries that is not in the m3u urls will be removed. This should be used with caution, if you add and remove m3u urls from the env variable often, then this will remove content from the VOD library. If your provider removes content often and you want to keep your VOD libraries in sync with what is available, then setting this to true is useful.

Default is set to `CLEAN_SYNC=false`

### LIVE TV STREAMS

Set `LIVE_TV=true` to generate a `livetv.m3u` file with all live TV streams from the provided m3u URLs. This file will be placed next to your VOD folders, /VODS/Live_TV

Default is set to: `LIVE_TV=true`

### UNSORTED

Set `UNSORTED=true` to create a VOD folder for poorly named or unidentified streams. This folder can be added manually to your Jellyfin server and edited through the web UI.

Default is set to `UNSORTED=false`

### ADDITIONAL OPTIONS

If you want to incorporate each of the Movie_VOD and TV_VOD folders into an existing library, then you can use these volume mounts below. Be careful, if you do this and have set `CLEAN_SYNC=true`, then this will remove any of your existing media in those host locations that are not present in the m3u urls. This is more than likely unwanted, so be sure to set `CLEAN_SYNC=false` if you do use the below mounts. (false is default value if CLEAN_SYNC is blank or absent from compose file)

```
volumes:
      - /path/to/your/media/library/tvshows:/usr/src/app/VODS/TV_VOD
      - /path/to/your/media/library/movies:/usr/src/app/VODS/Movie_VOD
      - /path/to/your/media/library/liveTVm3us:/usr/src/app/VODS/Live_TV
```
