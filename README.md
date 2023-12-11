# m3uparser
Parse your m3u VOD list and make a .strm library for media server

Docker Compose Example

```compose example
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
# Additional Options

While I suggest creating a folder named VODS in your media folder that your media server has access to,
you can also map the Movie VOD and the TV VOD to existing folders.

For example, if your current jellyfin server has a mapped volume like this:
/home/user/media/tvshows:/tvshows and one for movies like /home/user/media/movies:/movies
You could use this for your m3uparser volume mounts:
"/home/user/media/tvshows/:/VODS/TV VOD" and "/home/user/media/movies/:/VODS/Movie VOD".

Use the above at your own risk however, as the script that populates the Movie VOD and TV VOD folders
in the container at /VODS does delete movies and shows that do not appear in the m3ulist.

This more than likely will not touch your existing media that is those folders on your host machine,
but it has not been fully tested.

What the above does accomplish is having a single media library,
one for each TV and Movies in your jellyfin/emby/plex.

My suggestion is to map the folders to a folder accessible to jellyfin but not directly in an existing library.
So for example use /home/user/media/:/VODS
That will create the TV VOD and Movie VOD folders in the media folder,
and then add those as either new libraries to your media server, or, using jellyfin as an example,
edit your current TV Show and Movie library to include those VOD folders.

I myself seperate my VOD .strm library from my digital library. As in, in my jellyfin server I have each a Movies, TV Shows, Movie VOD, TV VOD library. This allows some flexability if for some reason a VOD library needs to be rebuilt or something goes wrong, it doesnt affect my non .strm library.
