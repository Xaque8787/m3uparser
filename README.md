![m3uparser](./parser/assets/other_img/logo.png)

m3u|>arser

m3u|>arser will parse your m3u urls and make a .strm library. Fill out the options in the compose file, run the container.

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
      - LIVE_TV= # Default is false, true will make a combined livetv.m3u from all 
      - UNSORTED= # Default is false, true will put Unsorted_VOD at same path as the 

    volumes:
      - /path/to/your/media/library:/usr/src/app/VODS
      - /path/to/your/media/library:/usr/src/app/logs/
```

| ENV VARIABLE  | VALUES                                              | DESCRIPTION                                                                                                   | EXAMPLE                                      | DEFAULT VALUES                      |
| ------------- |:---------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------:|:--------------------------------------------:|:-----------------------------------:|
| SCRUB_HEADER  | any text, in quotes, and seperated with a comma ,   | Removes value and preceding text from begining of group-title line                                            | "HD :"                                       | "HD :, SD :"                        |
| REMOVE_TERMS  | any text, in quotes, and seperated with a comma ,   | Removes value(s) set from file and directory names                                                            | "x264, 720p"                                 | "720p, WEB, h264, H264, HDTV, x264" |
| REPLACE_TERMS | "term-to-replace=replace-value"                     | Replaces one value with another. Separate terms with an = and term on left is replaced with term to the right | "replace-this=with-this"                     | "1/2=\u00BD, /=-"                   |
| CLEANERS      | series,movie,tv,unsorted                            | Type of stream to apply REMOVE_TERMS value to                                                                 | tv, movies                                   | tv                                  |
| LIVE_TV       | true/false                                          | Parse live tv streams in m3u urls and creates a single livetv.m3u                                             | true/false                                   | false                               |
| UNSORTED      | true/false                                          | Creates a VOD folder for undefined streams, either misspelled or poorly labeled streams                       | true/false                                   | false                               |
| M3U_URL       | any url(s), in quotes, and seperated with a comma , | Include all URLs you want to be parsed                                                                        | "https://m3u_URL1.com, https://m3u_URL2.com" | n/a                                 |
| HOURS         | numeric value                                       | Number representing the interval you want to update from m3u urls                                             | 12                                           | 8                                   |

## Basic Information

**Add more values to the environment variables in the compose file to extend the defaults.**

The parser uses the `group-title` value in the `#EXTINF` line of m3u files to structure the file and folder hierarchy. There are five stream types:

- **series**: Shows with season/episode values.
- **tv**: Shows with 'aired on date', such as talk shows with guest stars.
- **movies**: Movies with release years.
- **live-tv**: Live TV streams.
- **unsorted**: Streams that do not fit into the above categories.

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

### Jellyfin Integration

You must have a Jellyfin server accessible if using this script with the `API_KEY` and `JELLYFIN_URL` env variable. If you supply a address to your working server, and an api key you generated on that server; then when this script is ran it will refresh your library to include any titles that were added to the VOD libraries. If you have LIVE_TV=TRUE, then it will also refresh your tv guide. If you want to ommit the library scan you can add the environment variable `REFRESH_LIB=false`.

JELLYFIN_URL should include http:// or https:// (DO NOT SURROUND WITH "")
Logs will now be uploaded to the server as well.

### LIVE TV STREAMS

Set `LIVE_TV=true` to generate a `livetv.m3u` file with all live TV streams from the provided m3u URLs. This file will be placed next to your VOD folders.

Default is set to: `LIVE_TV=false`

### UNSORTED

Set `UNSORTED=true` to create a VOD folder for poorly named or unidentified streams. This folder can be added manually to your Jellyfin server and edited through the web UI.

Default is set to `UNSORTED=false`
