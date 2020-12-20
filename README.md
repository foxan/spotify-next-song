# spotify-next-song

When Spotify is being played on Google Home devices, the language set in Google Assistant will be used and request playback metadata from Spotify.

However, traditional Chinese support on many Google Nest devices are still missing, causing the default language to be in English and hence Spotify playback metadata as well:

![before](images/before.png)

This application gets the current playback from Spotify API every 60 seconds, and will skip the current track when the it almost ends.

As language preference can be provided when making API calls, this can work around the above issue by choosing the desired language.

![after](images/after.png)
