import asyncio
import configparser
import random
import spotipy
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from spotipy.oauth2 import SpotifyOAuth

# time left before skipping a song (in seconds)
skip_threshold = 7

config = configparser.ConfigParser()
config.read_file(open("config.ini"))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["DEFAULT"]["client_id"],
                                               client_secret=config["DEFAULT"]["client_secret"],
                                               redirect_uri="http://localhost:9000/callback/",
                                               scope="user-read-playback-state user-modify-playback-state"),
                     # specify Spotify to respond in Chinese
                     language="zh-TW")


def get_current_playback():
    """ get current song info, sleep for (time left - skip threshold) seconds, then skip song """
    results = sp.current_playback()
    if results is not None:
        # only proceed if song is played on Cast devices
        if results["device"]["type"] in ("CastVideo", "CastAudio"):
            time_left = (results["item"]["duration_ms"] - results["progress_ms"]) // 1000
            artist_name = results["item"]["artists"][0]["name"]
            song_name = results["item"]["name"]
            print(f'Now playing: {artist_name} - {song_name}, Time left: {timedelta(seconds=time_left)}, ', end="")

            # wait till song is expected to end in skip_threshold
            if time_left - skip_threshold > 0:
                sleep_for = time_left - round(random.uniform(skip_threshold - 4, skip_threshold), 2)
                print(f'Sleep for: {str(timedelta(seconds=sleep_for)).split("0000")[0]}')
                time.sleep(sleep_for)

            # need to check again as there may be actions (pause, skip, etc) in between
            results = sp.current_playback()
            time_left = (results["item"]["duration_ms"] - results["progress_ms"]) // 1000
            if time_left <= skip_threshold:
                sp.next_track()
                print(f'Time left: {time_left}s, song skipped')


scheduler = AsyncIOScheduler()
scheduler.add_job(get_current_playback, "interval", seconds=60, max_instances=5)
scheduler.start()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
