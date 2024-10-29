![EZPZTV](./parser/assets/banner-light.png)

# EZPZTV + m3u|>arser

EZPZTV automates the Jellyfin server configuration, while m3u|>arser will parse your m3u urls and make a .strm library for the media server. Fill out the options in the compose file, run the container stack, and everything will be configured and ready to go.

Docker Compose Example

```
services:
  EZPZTV:
    container_name: ezpztv
    image: xaque87/ezpztv:latest
    environment:
      - PUID=1000 # Defaults 1000 if blank.
      - PGID=1000 # Defaults 1000 if blank.
      - M3U_URL= # "https://m3u_URL1.com, https://m3u_URL2.com, etc..."
      - BYPASS_HEADER= # Optional, Set to true if you want to bypass checking content-type or content-disposition for m3u urls.
      - HOURS=12 # update interval, setting this optional, default 12hrs.
      - SCRUB_HEADER= # Optional, add more/different scrub values, does not override the defaults
      - EXCLUDE_TERMS= # Optional, exclude content that has defined term in the group-title value in m3u
      - REMOVE_TERMS= # Optional, add more/different remove term values, does not override the defaults
      - REPLACE_TERMS # Optional, add more/different replace values, does not override the defaults
      - CLEANERS= # Optional, add more/different cleaner values, does not override the defaults
      - CLEAN_SYNC= # If set to true will remove titles from VOD folders that are not present in m3u files, Defaults to false if blank.
      - LIVE_TV= # Default is true, true will make a combined livetv.m3u from all live tv streams in M3U_URL
      - EPG_URL="https://epg_url.com, https://epg2_url.com, etc..."
      - UNSORTED= # Default is false if blank, true will put Unsorted_VOD at same path as the other VOD folders.
      - REFRESH_LIB= # Default is false if blank. Will refresh libraries after each parsing.
      - USER_NAME=Choose_Username # Username that will be used to log into the server.
      - PASSWORD=Choose_Password # Password that will be used to log into the server.

    volumes:
      - movie_vod_volume:/usr/src/app/VODS/Movie_VOD/
      - tv_vod_volume:/usr/src/app/VODS/TV_VOD/
      - live_tv:/usr/src/app/VODS/Live_TV/
      - server_cfg_volume:/usr/src/app/server_cfg/
      - branding:/usr/src/app/branding
    networks:
      ezpznet:
        ipv4_address: 10.21.12.7
      default:

  ezpztv_server:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: Jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    # - JELLYFIN_PublishedServerUrl=0.0.0.0 #optional
    volumes:
      - config_volume:/config
      - tv_vod_volume:/data/tvshows
      - movie_vod_volume:/data/movies
      - live_tv:/data
      - branding:/usr/share/jellyfin/
    ports:
      - 8096:8096
      - 8920:8920 # optional
      - 7359:7359/udp # optional
      - 1900:1900/udp # optional
    networks:
      ezpznet:
        ipv4_address: 10.21.12.8
      default:
    restart: unless-stopped

networks:
  ezpznet:
    ipam:
      driver: default
      config:
        - subnet: "10.21.12.0/28"

volumes:
  server_cfg_volume:
  live_tv:
  movie_vod_volume:
  tv_vod_volume:
  config_volume:
  branding:
```

| ENV VARIABLE  | VALUES                                              | DESCRIPTION                                                                                                   | EXAMPLE                                      | DEFAULT VALUES                     |
| ------------- |:---------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------:|:--------------------------------------------:|:----------------------------------:|
| M3U_URL       | any url(s), in quotes, and seperated with a comma , | Include all URLs you want to be parsed                                                                        | "https://m3u_URL1.com, https://m3u_URL2.com" | n/a                                |
| BYPASS_HEADER | true/false                                          | Bypass checking url header for content-type and content-disposition.                                          | False                                        | False                              |
| HOURS         | numeric value                                       | Number representing the interval you want to update from m3u urls                                             | 12                                           | 8                                  |
| SCRUB_HEADER  | any text, in quotes, and seperated with a comma ,   | Removes value and preceding text from begining of group-title line                                            | "HD :"                                       | "HD :, SD :"                       |
| EXCLUDE_TERMS | any text, in quotes, and seperated with a comma ,   | Excludes content that contains defined term if found in the group-title                                       | "AR -, FR -"                                 | ""                                 |
| REMOVE_TERMS  | any text, in quotes, and seperated with a comma ,   | Removes value(s) set from file and directory names                                                            | "x264, 720p"                                 | "720p, WEB, h264,H264, HDTV, x264" |
| REPLACE_TERMS | "term-to-replace=replace-value"                     | Replaces one value with another. Separate terms with an = and term on left is replaced with term to the right | "replace-this=with-this"                     | "1/2=\u00BD, /=-"                  |
| CLEANERS      | series,movie,tv,unsorted                            | Type of stream to apply REMOVE_TERMS value to                                                                 | tv, movies                                   | tv                                 |
| REFRESH_LIB   | true/false                                          | Refresh Jellyfin libraries after parsing                                                                      | false                                        | false                              |
| CLEAN_SYNC    | true/false                                          | Will remove titles from VOD folders that are not present in m3u.                                              | false                                        | false                              |
| LIVE_TV       | true/false                                          | Parse live tv streams in m3u urls and creates a single livetv.m3u                                             | true/false                                   | true                               |
| UNSORTED      | true/false                                          | Creates a VOD folder for undefined streams, either misspelled or poorly labeled streams                       | true/false                                   | false                              |
| USER_NAME     | Pick-a-Username                                     | Choose a username for the admin user of the server                                                            | majordude                                    | n/a                                |
| PASSWORD      | Pick-a-Password                                     | Choose a password for the admin user of the server                                                            | some_password                                | n/a                                |

## Instalation Process

```
mkdir ezpztv
cd ezpztv
curl -o docker-compose.yaml https://raw.githubusercontent.com/Xaque8787/m3uparser/ezpztv/ezpztv/docker-compose.yaml
curl -o ezpztv.env https://raw.githubusercontent.com/Xaque8787/m3uparser/ezpztv/ezpztv/ezpztv.env
```

Then edit the ezpztv.env file with your credentials and desired values.

Then run:

```
docker compose up -d
```

##### EZPZTV APK for Fire TV and Google Tv

To install the EZPZTV Fire TV app for firesticks or Google TV devices.

In the .env file set APK value to true `APK=true`

In the compose file un comment the ports: section

`ports:
    - 2112:2112`

After starting the container, once the script has initially ran, use Downloader app for Fire TV and go to your servers ip address and port 2112. This will automatically start the download of the EZPZTV apk, and once download is complete you can install it. The webserver serving the apk file will close automatically after a single download, you can then remove APK=true and the port mapping from the compose file. If you do not though, it will not start the webserver on subsequent runs. If you need to install the apk again you can run the command

`docker exec -it ezpztv /bin/bash -c "python3 parser/server_apk/apk.py"`

## Basic m3u Parsing Information

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

Example: `SCRUB_HEADER="HD :, SD :"`. This removes these values, if they exist, and any preceding text from the `group-title` line. So a line like this, `group-title="Movie VOD",HD : The Fall Guy 2024` will become `group-title= The Fall Guy 2024`. Ensure spaces are included where needed. Add multiple values to `SCRUB_HEADER=`, separated by commas, in a single set of quotes. You can escape charcters like , or " but using a \ `SCRUB_HEADER="Movie VOD\,"` If you need to escape " that string must not be the first or last in the defined list, and you may add "dummy" values to avoid this. So if your group-title looks like this `group-title="Movie VOD",The Fall Guy 2024`, your SCRUB_HEADER value should look like this `SCRUB_HEADER="dummyvalue, \"Movie VOD\"\,, fakevalue"`

Default is set to: `SCRUB_HEADER="HD :, SD :"`

### REMOVE_TERMS & CLEANERS

`REMOVE_TERMS` removes specified terms, and any attatched text, from titles. For instance, `REMOVE_TERMS="x264"`, would remove the entire string `x264-somegarbge`. This setting is case-sensitive and should have multiple values separated by commas, in a single set of quotes. i.e `REMOVE_TERMS="x264, h264, X264"`

Default is set to: `"720p, WEB, h264, H264, HDTV, x264"`

The `CLEANERS` variable defines which stream types `REMOVE_TERMS` applies to. For example, `CLEANERS=series,tv` applies `REMOVE_TERMS` to series and TV shows.

Default is set to: `tv`

### REPLACE_TERMS

Add more replacements to `REPLACE_TERMS` in the format `"replace=value"`. For example: `REPLACE_TERMS="replace-this=with-this, dontwant=wantinstead"`. This replaces specified terms in all streams, except live TV.

Default is set to: `"1/2=\u00BD, /=-"`

### LIVE TV STREAMS & EPG_URL

Set `LIVE_TV=true` to generate a `livetv.m3u` file with all live TV streams from the provided m3u URLs. This file will be placed next to your VOD folders, and will be picked up by EZPZTV for configuring live tv tuners.

Default is set to: `LIVE_TV=true`

If you supply url(s) to the `EPG_URL=` variable, they will be added as xmltv guide data in the server. Put value inside double quotes, and seperate urls with a comma.

`EPG_URL= https://epgurl1.com, http://anotherepg.com"`

### REFRESH_LIB

The default for EZPZTV is to set libraries to real time monitoring. So content is added picked up on the server when it is added from a parser run (interval you set). However you can force a library refresh every interval by setting `REFRESH_LIB=true` in your compose or ezpztv.env file.

Default is set to `REFRESH_LIB=false`

### BYPASS_HEADER

Setting this to true will have the script download the m3u urls regardless if it is available from provider or not. It will still check for 200 response from url, but will not check for content-type or content-disposition from the header response. These two checks are useful for ensuring the m3u file downloaded is actually available from the provider. In some cases if your provider is "down", you still may get a 200ok response from their server, but the m3u file that will be downloaded will be empty, resulting in a failed parsing. There are cases where the provider does not have a content-disposition entry in their url header response, so setting this env variable to false will bypass this check and download the m3u file regardless. 

### CLEAN_SYNC

If this is set to true, then every time a parsing of m3u urls is complete, it will add new content from the m3u urls to your VOD libraries, and any content in your VOD libraries that is not in the m3u urls will be removed. This should be used with caution, if you add and remove m3u urls from the env variable often, then this will remove content from the VOD library. If your provider removes content often and you want to keep your VOD libraries in sync with what is available, then setting this to true is useful.

Default is set to `CLEAN_SYNC=false`

### UNSORTED

Set `UNSORTED=true` to create a VOD folder for poorly named or unidentified streams. This folder can be added manually to your Jellyfin server and edited through the web UI.

Default is set to `UNSORTED=false`

## Additional Options

If you encounter issues, run `docker compose down -v` and restart the container. If problems persist, enter the container and check the log file:

```
docker exec -it ezpztv /bin/bash
cat "/usr/src/app/logs/log_file.log"
```

For active monitoring of logs run:

```
docker exec -it ezpztv /bin/bash -c "tail -f ./logs/log_file.log"
```

For real-time monitoring issues, increase the inotify watch limit on your host machine:

```
sudo sh -c "echo fs.inotify.max_user_watches=524288 >> /etc/sysctl.conf"
sudo sysctl -p
```

Refer to the [Jellyfin troubleshooting guide](https://jellyfin.org/docs/general/administration/troubleshooting/#real-time-monitoring) for more details.
