# m3uparser
Parse your m3u VOD list and make a .strm library for media server

Docker Compose Example

```
version: '3'

services:
  m3uparser:
    image: xaque87/m3uparser
    environment:
      - VOD_URL=<YOUR_IPT_VOD_M3U_URL>
      - HOURS=12 #optional, defaults to 12hrs if you ommit this line, suggest not going below 6hrs.
    volumes:
      - /path/to/your/media/library:/VODS

```
