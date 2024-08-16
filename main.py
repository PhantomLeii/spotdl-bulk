from spotipy.oauth2 import SpotifyClientCredentials
from typing import List, Tuple, Dict
import spotipy, os, time, requests

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    artists = read_artists("artists.txt")
    for artist in artists:
        artist_id = get_artist_id(artist)
        albums = get_albums(artist_id)

        print(f"=== Downloading {artist} albums... ===")
        artist_dir = f"{BASE_DIR}/{artist}"
        if not os.path.exists(artist_dir):
            os.makedirs(artist_dir)
        
        os.chdir(artist_dir)
        
        for album in albums:
            status = download(album)
            if status == 1:
                continue
    print("=== All downloads completed ===")

        

def read_artists(file_path: str) -> Tuple[str]:
    """Read artist names from file."""
    artists = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                artists.append(line.strip().title())
    except FileNotFoundError:
        print(
            f"=== File, '{file_path}' file not found. Create one and populate it with artist names. ==="
        )
    return tuple(artists)


def get_artist_id(artist_name: str, retries:int=3, delay:int=10) -> str|None:
    """Get artist ID from spotify API."""
    try:
        res = sp.search(q=f"artist:{artist_name}", type="artist")
        aritst_id = res['artists']['items'][0]['id']
        return aritst_id
    except requests.exceptions.ReadTimeout:
        if retries > 0:
            print(f"=== Error: Read timeout. Retrying... ===")
            time.sleep(delay)
            get_artist_id(artist_name, retries-1, delay*2)
        else:
            print(f"=== Error: Could not search {artist_name}. ===")
            return None

def get_albums(artist_id: str, retries:int=3, delay:int=10) -> Tuple[str]:
    """Get all albums of an artist."""
    albums = []
    try:
        res = sp.artist_albums(artist_id, include_groups="album,single", limit=50)
        for album in res['items']:
            albums.append(album['external_urls']['spotify'])
        return tuple(albums)
    except requests.exceptions.ReadTimeout:
        if retries > 0:
            print(f"=== Error: Read timeout. Retrying... ===")
            time.sleep(delay)
            get_albums(artist_id, retries-1, delay*2)
        else:
            print(f"=== Error: Could not get albums for {artist_id}. ===")
            return None


def download(album_url: str, retries:int=3, delay:int=10) -> int:
    """Download album from spotify URL."""
    if retries < 1:
        print(f"=== Error: Could not download {album_url}. ===")
        return 1
    
    res_code = os.system(f"spotdl download {album_url}")
    if res_code != 0:
        print(f"=== Error: Could not download {album_url}. Retrying... ===")
        time.sleep(5)
        download(album_url, retries-1, delay*2)

    return 0


if __name__ == "__main__":
    main()