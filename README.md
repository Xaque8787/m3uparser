<<<<<<< HEAD
# m3u|>arser / EZPZTV
Parse your m3u urls and make a .strm library for media server. 

Notice that the docker image is now **xaque87/ezpztv:latest**

By adding this jellyfin service section to the compose file m3u|>arser will automatically setup a jellyfin server via API calls.

Make sure to not change volume mounts or the ezpz network ip addresses, they are crucial to the setup.

Access to your server will be on localhost, local ip address, or ezpznet address. To connect to your server from another device use local_ip_address:8096

You can also un comment out the #- JELLYFIN_PublishedServerUrl=0.0.0.0 line in the Jellyfin service to set a different ip address to connect to from the server.
```
services:
  ezpztv:
    container_name: ezpztv
    image: ezpztv:test
=======
m3u|>arser & EZPZTV

Parse your m3u urls and make a .strm library for media server.

Notice that the docker image is now xaque87/ezpztv:latest

By adding this jellyfin service section to the compose file m3u|>arser will automatically setup a jellyfin server via API calls.

Make sure to not change volume mounts or the ezpz network ip addresses, they are crucial to the setup.

Access to your server will be on localhost, local ip address, or ezpznet address. To connect to your server from another device use local_ip_address:8096

You can also un comment out the #- JELLYFIN_PublishedServerUrl=0.0.0.0 line in the Jellyfin service to set a different ip address to connect to from the server.

services:
  ezpztv:
    container_name: ezpztv
    image: ezpztv:latest
>>>>>>> ezpztv_test
    environment:
      - PUID=1000
      - PGID=1000
      - M3U_URL="<YOUR M3U urls, can add multiple urls, and they can contain a mix of VOD and TV>"
      - HOURS=12 # update interval, setting this optional, defaults to 12hrs if you omit this line, suggest not going below 6hrs.
      - SCRUB_HEADER=
      - REMOVE_TERMS=
      - CLEANERS=
      - USER_NAME=Enter_A_Username
      - PASSWORD=Enter_A_Password
      - EPG_URL="<ENTER a EPG url>"
      - LIVE_TV=true/false #Set to true to have a livetv.m3u created from  any live tv streams found in M3U urls, and auto populate to Jellyfin.
      - SERVER_NAME=Enter_A_Name to identify your server # Optional
      - UNSORTED=true/false #If true then Unsorted_VOD folder will populate at mount path, but not be added to the server.
    volumes:
      - movie_vod_volume:/usr/src/app/VODS/Movie_VOD/
      - tv_vod_volume:/usr/src/app/VODS/TV_VOD/
      - live_tv:/usr/src/app/VODS/Live_TV/
    networks:
      ezpznet:
        ipv4_address: 10.21.12.7
      default:
<<<<<<< HEAD

  ezpztv_jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: ezpztv_jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      #- JELLYFIN_PublishedServerUrl=0.0.0.0 #optional
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
  live_tv:
  movie_vod_volume:
  tv_vod_volume:
  config_volume:
```
=======
>>>>>>> ezpztv_test

  ezpztv_jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: ezpztv_jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      #- JELLYFIN_PublishedServerUrl=0.0.0.0 #optional
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
  live_tv:
  movie_vod_volume:
  tv_vod_volume:
  config_volume:

ENV VARIABLE 	VALUE 	DESCRIPTION 	EXAMPLE
SCRUB_HEADER 	any text, in quotes, and seperated with a comma , 	Removes value and preceeding text from begining of group-title line 	"HD :"
REMOVE_TERMS 	any text, in quotes, and seperated with a comma , 	Removes value(s) set from file and directory names, requires at least 1 CLEANER value set 	"x264, 720p"
CLEANERS 	series,movie,tv,unsorted 	Type of stream to apply REMOVE_TERMS value to 	tv, movies
LIVE_TV 	true/false 	Parse live tv streams in m3u urls and creates a single livetv.m3u 	true/false
UNSORTED 	true/false 	Creates a VOD folder for undefined streams, either misspelled or poorly labled streams 	true/false
Basic Information

Most of the information used to create the file and folder structure is derived from the group-title value in the m3u files #EXTINF line. There are 5 types of streams that are defined.

    series - Television shows that have season/episode value

    tv - Television shows that use 'aired on date'. Typically late night talk shows that contain a guest star in the title. i.e. Jimmy Kimmel Chris Pine 2024 05 09 or The Daily Show Matt Damon 2024 05 08

    movies - Movies with year release

    live-tv - Any stream that is a live tv stream.

    unsorted - Any stream found that does not fit the above

Examples and Explanations

SCRUB_HEADER

First thing to do would be to look at a line from one or all of the m3u files you plan to parse. The SCRUB_HEADER value should be a string of characters that is in each 'group-title=' value of the #EXTINF line. Take the below as an example, you can see that in each of the group-title= value that there is the string "Movie VOD",HD : that comes before each movie title and year. To "scrub" this line, you could add "HD :" to the SCRUB_HEADER value in the compose, and it will remove the value + everything that precedes it. This is required to correctly parse the titles, year, and other information for TV and Movies. The SCRUB_HEADER function is applied to all lines in thr m3u file, while REMOVE_TERMS is applied to all titles that are set in the CLEANERS value, while live tv streams are processed seperatly without SRUB_HEADER or REMOVE_TERMS applied.

#EXTINF:0 group-title="Movie VOD",HD : The Crow 1994
#EXTGRP:Movie VOD
https://streamurl.from.provider
#EXTINF:0 group-title="Movie VOD",HD : Total Recall 2012
#EXTGRP:Movie VOD
https://streamurl.from.provider

You can add multiple SCRUB_HEADER values to accomodate varying m3u naming formats. All values go in a single set of quotes, and are seperated by commas. SCRUB_HEADER="HD :, SD :"

Trailing whitespaces will be stripped, so in this example you do not need to add a space after the : but the space in beween HD and the : will and should be included in the SCRUB_HEADER value.

REMOVE_TERMS & CLEANERS

Similar to the SCRUB_HEADER but removes the value of the term + any attatched characters. For titles that have "x264-somegarbage", your REMOVE_TERMS value should be x264. This will remove the entire 'x264-somegarbage' line. This is case sensitive, so it is best to include both variations for values. A typical REMOVE_TERMS line in a compose file would look like REMOVE_TERMS="x264, X264, HDTV, WEB, 720, x265, X265". The REMOVE_TERMS will only apply to titles of values in the CLEANERS. So, if you find that only series (TV that has seasons and episodes) and tv shows (shows with 'air-date') then your CLEANERS line in the compose file should be CLEANERS=series,tv

    series = shows with season/episodes, tv = shows with 'air-dates', movie = movie, unsorted = unsorted

LIVE TV STREAMS

Any m3u url supplied in the compose file will work with mixed live-tv/VOD content. It will take any live tv stream and create a livetv.m3u that contains any live tv stream found in any of the m3u urls. If you want to have this livetv.m3u file, set LIVE_TV=true in the compose file, and it will appear next to your VOD folders at the specified volume mount.

UNSORTED

Any unidentified movie or show will end up in this folder. It normally is because; the movie title lacks a release date, random numbers at the end of the show or movie title, or some other poorly named title from the provider. To have this folder placed next to your other VOD folders, set UNSORTED=true
Additional Options

I suggest creating a folder named VODS that your media server has access to. Or a more direct way may be is to map the folders to a directory accessible to Jellyfin, but not directly in an existing library. So for example, in m3uparser compose file use volume /home/user/media/:/usr/src/app/VODS. Then in your jellyfin compose file have /home/user/media/:/data/

That will create the TV VOD and Movie VOD folders in the directory that Jellyfin can access, and then add those as either new libraries,or edit your current TV Show and Movie library to include those VOD folders.

I myself separate my VOD .strm library from my digital library. As in, in my jellyfin server I have each a Movies, TV Shows, Movie VOD, TV VOD library. This allows some flexibility if for some reason a VOD library needs to be rebuilt or something goes wrong, it doesnt affect my non .strm library. However, either way should work just fine.

