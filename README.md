![EZPZTV](logo.png)


# m3u|>arser with EZPZTV
Parse your m3u urls and make a .strm library for media server

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
      - HOURS=12 # update interval, setting this optional, default 12hrs.
      - SCRUB_HEADER= # Optional, add more/different scrub values, does not override the defaults
      - REMOVE_TERMS= # Optional, add more/different remove term values, does not override the defaults
      - REPLACE_TERMS # Optional, add more/different replace values, does not override the defaults
      - CLEANERS= # Optional, add more/different cleaner values, does not override the defaults
      - LIVE_TV= # Default is false, true will make a combined livetv.m3u from all live tv streams in M3U_URL
      - UNSORTED= # Default is false, true will put Unsorted_VOD at same path as the other VOD folders.
      - USER_NAME=Choose_Username # Username that will be used to log into the server.
      - PASSWORD=Choose_Password # Password that will be used to log into the server.
      - EPG_URL="https://epg_url.com, https://epg2_url.com, etc..."
    volumes:
      - movie_vod_volume:/usr/src/app/VODS/Movie_VOD/
      - tv_vod_volume:/usr/src/app/VODS/TV_VOD/
      - live_tv:/usr/src/app/VODS/Live_TV/
      - server_cfg_volume:/usr/src/app/server_cfg/
    networks:
      ezpznet:
        ipv4_address: 10.21.12.7
      default:

  Jellyfin:
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
```

| ENV VARIABLE  | VALUE  | DESCRIPTION | EXAMPLE | DEFAULT VALUES |
| :------------ |:-------:|:-----:|:-----|:-----:|
|SCRUB_HEADER|any text, in quotes, and seperated with a comma ,|Removes value and preceding text from begining of group-title line|"HD :"|"HD :, SD :"|
|REMOVE_TERMS|any text, in quotes, and seperated with a comma ,|Removes value(s) set from file and directory names|"x264, 720p"| "720p, WEB, h264, H264, HDTV, x264"|
|REPLACE_TERMS|"term-to-replace=replace-value"|Replaces one value with another. Separate terms with an = and term on left is replaced with term to the right|"replace-this=with-this"| "1/2=\u00BD, /=-"|
|CLEANERS|series,movie,tv,unsorted|Type of stream to apply REMOVE_TERMS value to| tv, movies|tv|
|LIVE_TV|true/false|Parse live tv streams in m3u urls and creates a single livetv.m3u|true/false|false|
|UNSORTED|true/false|Creates a VOD folder for undefined streams, either misspelled or poorly labeled streams|true/false|false|

### Basic Information

You can see the log from each time the parser script runs by going to Jellyfin>dashboard>logs>ezpztv_logs
 
Most of the information used to create the file and folder structure is derived from the group-title value in the m3u files #EXTINF line.
There are 5 types of streams that are defined.

+ series - Television shows that have season/episode value

+ tv - Television shows that use 'aired on date'. Typically late night talk shows that contain a guest star in the title. i.e. Jimmy Kimmel Chris Pine 2024 05 09 or The Daily Show Matt Damon 2024 05 08

+ movies - Movies with year release

+ live-tv - Any stream that is a live tv stream.

+ unsorted - Any stream found that does not fit the above


## Examples and Explanations

### **DEFAULT VALUES**
All default values can be added to by entering more values into the appropriate env variable in the compose file.

### **SCRUB_HEADER**

**You can add multiple SCRUB_HEADER values to accommodate varying m3u naming formats. All values go in a single set of quotes, and are separated by commas. SCRUB_HEADER="HD :, SD :"**

**Trailing whitespaces will be stripped, so in this example you do not need to add a space after the : but the space in between HD and the : will and should be included in the SCRUB_HEADER value.**


If you need to add more scrub header values, the first thing to do would be to look at a line from one or all of the m3u files you plan to parse. The SCRUB_HEADER value should be a string of characters that is in each 'group-title=' value of the #EXTINF line. Take the below as an example, you can see that in each of the group-title= value that there is the string **"Movie VOD",HD :** that comes before each movie title and year. To "scrub" this line, you could add "HD :" to the SCRUB_HEADER value in the compose, and it will remove the value + everything that precedes it. This is required to correctly parse the titles, year, and other information for TV and Movies. The SCRUB_HEADER function is applied to all lines in the m3u file, while REMOVE_TERMS is applied to all titles that are set in the CLEANERS value, and live tv streams are processed separately without SCRUB_HEADER or REMOVE_TERMS applied.

Example of m3u file, where SCRUB_HEAD="HD :" will leave a clean movie title entry.
```
#EXTINF:0 group-title="Movie VOD",HD : The Crow 1994
#EXTGRP:Movie VOD
https://streamurl.from.provider
#EXTINF:0 group-title="Movie VOD",HD : Total Recall 2012
#EXTGRP:Movie VOD
https://streamurl.from.provider
```
### **REMOVE_TERMS & CLEANERS**

Similar to the SCRUB_HEADER but removes the value of the term + any attatched characters. For titles that have "**x264-somegarbage**", your REMOVE_TERMS value should be x264. This will remove the entire 'x264-somegarbage' line. This is case sensitive, so it is best to include both variations for values. A typical REMOVE_TERMS line in a compose file would look like REMOVE_TERMS="x264, X264, HDTV, WEB, 720, x265, X265" *this is now the default. The REMOVE_TERMS will only apply to titles of values in the CLEANERS. So, if you find that only series (TV shows that have seasons and episodes) and tv shows (shows with 'air-date') then your CLEANERS line in the compose file should be CLEANERS=series,tv. **tv category is now set to default for cleaners.** Another example of using these env vars would be if your movie titles contain a language in them, i.e Tropic Thunder [SP] (2012). So the [SP] would be the term you put in ```REMOVE_TERMS="[SP]"``` and add movies to ```CLEANERS=movies```

>series = shows with season/episodes, tv = shows with 'air-dates', movie = movie, unsorted = unsorted

### **REPLACE TERMS**

The default for REPLACE_TERMS is "1/2=\u00BD, /=-" which will take 1/2 and replace it with the unicode character &frac12; And replace any / with a -

To add more add more terms to replace, add them to REPLACE_TERMS= in your compose file. The format is

 ```REPLACE_TERMS="replace=value"``` Where the term you want replaced is to the left of the = sign, and teh value to replace it with is to the right. Separate multiple replacement terms with a , ```REPLACE_TERMS="replace=value, this=that, dont_want=want_instead"```

REPLACE_TERMS is a applied to all types of streams except for live tv.

### **LIVE TV STREAMS**

Any m3u url supplied in the compose file will work with mixed live-tv/VOD content. It will take any live tv stream and create a livetv.m3u that contains any live tv stream found in all of the m3u urls. If you want to have this livetv.m3u file, set LIVE_TV=true in the compose file, and it will appear next to your VOD folders at the specified volume mount, where it will be added to the Jellyfin server.

### **UNSORTED**

Any unidentified movie or show will end up in this folder. It normally is because; the movie title lacks a release date, random numbers at the end of the show or movie title, or some other poorly named title from the provider. To have this folder placed next to your other VOD folders, set UNSORTED=true. You can then add this as a library to your Jellyfin server manually, and use the web-ui to edit the titles to their appropriate value.

### Additional Options

If something goes wrong with the initial setup, from the directory of the compose file run 'docker compose down -v' and then try restarting the container. If that does not work, run the container then:
```
docker exec -it ezpztv /bin/bash
cat "/usr/src/app/logs/log_file.log"
```

Real time monitoring is enabled for all media libraries, and after the first library scan completes, the scheduled task for preforming a library scan will be disabled. If you have trouble getting new items to populate in the recently added section, then this may be an issue with inotify. See Jellyfin docs here about this issue and resolution https://jellyfin.org/docs/general/administration/troubleshooting/#real-time-monitoring or the github here for more details https://github.com/guard/listen?tab=readme-ov-file#the-technical-details

Running the command below on your host (not in the container) will more than likely resolve the issue.
```
$ sudo sh -c "echo fs.inotify.max_user_watches=524288 >> /etc/sysctl.conf"
$ sudo sysctl -p
```
