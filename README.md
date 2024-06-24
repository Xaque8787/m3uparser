# m3u|>arser
Parse your m3u urls and make a .strm library for media server

Docker Compose Example

```compose example
services:
  m3uparser:
    image: xaque87/m3uparser:latest
    environment:
      - PUID=1000 # Default if blank
      - PGID=1000 # Default if blank
      - M3U_URL="m3uURL1.com, m3uURL2.com, etc..."
      - HOURS=12 #update interval, setting this optional, default 12hrs
      - SCRUB_HEADER= #required, probably. See below explanation and examples.
      - REMOVE_TERMS=
      - CLEANERS=
      - LIVE_TV= # Default is false
      - UNSORTED= # Default is false
    volumes:
      - /path/to/your/media/library:/usr/src/app/VODS
```

| ENV VARIABLE  | VALUE  | DESCRIPTION | EXAMPLE |
| :------------ |:-------:|:-----:|:-----|
|SCRUB_HEADER|any text, in quotes, and seperated with a comma ,|Removes value and preceeding text from begining of group-title line|"HD :"|
|REMOVE_TERMS|any text, in quotes, and seperated with a comma ,|Removes value(s) set from file and directory names, requires at least 1 CLEANER value set|"x264, 720p"|
|CLEANERS|series,movie,tv,unsorted|Type of stream to apply REMOVE_TERMS value to| tv, movies|
|LIVE_TV|true/false|Parse live tv streams in m3u urls and creates a single livetv.m3u|true/false|
|UNSORTED|true/false|Creates a VOD folder for undefined streams, either misspelled or poorly labled streams|true/false|

### Basic Information

Most of the information used to create the file and folder structure is derived from the group-title value in the m3u files #EXTINF line.
There are 5 types of streams that are defined.

+ series - Television shows that have season/episode value

+ tv - Television shows that use 'aired on date'. Typically late night talk shows and contain a guest star in the title. i.e. Jimmy Kimmel Chris Pine 2024 05 09 or The Daily Show Matt Damon 2024 05 08

+ movies - Movies with year release

+ live-tv - Any stream that is a live tv stream.

+ unsorted - Any stream found that does not fit the above


### Examples and Explanations
**SCRUB_HEADER**

First thing to do would be to look at a line from one or all of the m3u files you plan to parse. The SCRUB_HEADER value should be a string of characters that is in each 'group-title=' value of the #EXTINF line. Take the below as an example, you can see that in each of the group-title= value that there is the string **"Movie VOD",HD :** that comes before each movie title and year. To "scrub" this line, you could add "HD :" to the SCRUB_HEADER value in the compose, and it will remove the value + everything that precedes it. This is required to correctly parse the titles, year, and other information for TV and Movies. The SCRUB_HEADER function is applied to all lines in thr m3u file, while REMOVE_TERMSis applied to titles set in the CLEANERS value, and live tv streams are processed seperatly.
```
#EXTINF:0 group-title="Movie VOD",HD : The Crow 1994
#EXTGRP:Movie VOD
https://streamurl.from.provider
#EXTINF:0 group-title="Movie VOD",HD : Total Recall 2012
#EXTGRP:Movie VOD
https://streamurl.from.provider
```
You can add multiple SCRUB_HEADER values to accomodate varying m3u naming formats. All values go in a single set of quotes, and are seperated by commas. SCRUB_HEADER="HD :, SD :"

Trailing whitespaces will be stripped, so in this example you do not need to add a space after the : but the space in beween HD and the : will and should be included in the SCRUB_HEADER value.

**REMOVE_TERMS & CLEANERS**

Similar to the SCRUB_HEADER but removes the value of the term + any attatched characters. For titles that have "**x264-somegarbage**", your REMOVE_TERMS value should be x264. This will remove the entire 'x264-somegarbage' line. This is case sensitive, so it is best to include both variations for values. A typical REMOVE_TERMS line in a compose file would look like REMOVE_TERMS="x264, X264, HDTV, WEB, 720, x265, X265". The REMOVE_TERMS will only apply to titles of values in the CLEANERS. So, if you find that only series (TV that has seasons and episodes) and tv shows (shows with 'air-date') then your CLEANERS line in the compose file should be CLEANERS=series,tv 

>series = shows with season/episodes, tv = shows with 'air-dates', movie = movie, unsorted = unsorted

**LIVE TV STREAMS**

Any m3u url supplied in the compose file will work with mixed live-tv/VOD content. It will take any live tv stream and create a livetv.m3u that contains any live tv stream found in any of the m3u urls. If you want to have this livetv.m3u file, set LIVE_TV=true in the compose file, and it will appear next to your VOD folders at the specified volume mount.

**UNSORTED**

Any unidentified movie or show will end up in this folder. It normally is because; the movie title lacks a release date, random numbers at the end of the show or movie title, or some other poorly named title from the provider. To have this folder placed next to your other VOD folders, set UNSORTED=true

### Additional Options

I suggest creating a folder named VODS that your media server has access to. Or a more direct way may be is to map the folders to a directory accessible to Jellyfin, but not directly in an existing library. So for example, in m3uparser compose file use volume /home/user/media/:/usr/src/app/VODS. Then in your jellyfin compose file have /home/user/media/:/data/ 

That will create the TV VOD and Movie VOD folders in the directory that Jellyfin can access, and then add those as either new libraries,or edit your current TV Show and Movie library to include those VOD folders.

I myself separate my VOD .strm library from my digital library. As in, in my jellyfin server I have each a Movies, TV Shows, Movie VOD, TV VOD library. This allows some flexibility if for some reason a VOD library needs to be rebuilt or something goes wrong, it doesnt affect my non .strm library. However, either way should work just fine.

