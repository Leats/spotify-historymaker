# Spotify Historymaker

I listen to a lot of Spotify music. As most Spotify users know, at the end of the year they summarize your year of music for you. It is one of the things I really look forward to, because it combines both statistics and music together. But I did want something more detailed. And I wanted more control over what I would be shown.

[Spotify's API](https://developer.spotify.com/documentation/web-api/reference) is able to give out the top artists and tracks but not more than that regarding long-time use. However, it also allows to give specific information about the user's recently played songs (limited to 50).
This is what I use to collect statistics in a PostgreSQL database.

I decided on several different tables for the played song (including timestamp), the context (if available), the track itself, the artist and the album.

-------
## How to use

A PostgreSQL database needs to be in place. The schema for this can be found in `dump.sql`. 

Follow [Spotify's guide](https://developer.spotify.com/documentation/general/guides/app-settings/) to create a client id (and secret). Follow through until you have a refresh token you can use. The Authorization Scope needed for this script is `user-read-recently-played`.

`exampleconfig.ini` needs to get changed:
  * fill in the details of your database
  * fill in the client id, secret and refresh token from the last step
  * save as config.ini in the same directory
  
 Make sure you have all requirements from `requirements.txt` installed.
 
 **You should now be able to run the script.** To get the most out of the script it will have to be run regularly, resulting in a continuous logging of the recently played tracks. Looking at [Spotify's reference for Recently Played Tracks](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/) it can be calculated that with a time of 25 minutes inbetween will be enough to ensure a full coverage since the last 50 songs can be returned by Spotify and a song has to play at least 30 seconds to be counted.
