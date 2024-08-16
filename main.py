from spotipy.oauth2 import SpotifyClientCredentials
from typing import List, Tuple, Dict
import spotipy, os, time

CLIENT_ID = "b15dccc7e05b4f90bf350da6ff1e0be8"
CLIENT_SECRET = "67313c18a40c474d90b25b8f89ea1b16"

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def main():
    print("Hello world!")


if __name__ == "__main__":
    main()