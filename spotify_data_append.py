import pandas as pd
import numpy as np

from spotify_config import spotify_headers

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Set up requests session and to account for retries should connection errors arise.
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def encode_spaces(string_list):
    '''Replaces spaces with %20 for Spotify API search'''
    encoded = [string.replace(" ", "%20") for string in string_list]
    return encoded


def clean_search_terms(string):
    '''Cleans up string for spotify search.'''
    cleaned = string.replace("%20Featuring%20","%20")    .replace("%20X%20","%20")    .replace("%20x%20","%20")    .replace("%20VS%20","%20")    .replace("%20VS%20","%20")    .replace("#","")
    return cleaned


def get_track_ids(artists, songs):
    '''Returns a list of track IDs for songs. Takes in two lists as arguments. '''
    track_id_list = []

    for artist,song in zip(encode_spaces(artists),encode_spaces(songs)):
        print("-"*20)
        print("Searching Spotify API for...")
        print(artist.replace("%20"," "), song.replace("%20"," "))
        print("-"*20)

        # Further format search terms for artists to get better results.
        artist_ = clean_search_terms(artist)
        
        # Form query
        query = artist_+"%20"+song
        base_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"

        response = session.get(base_url,headers=spotify_headers).json()
        
        try:
            track_id = response['tracks']['items'][0]['id']
            track_name = response['tracks']['items'][0]['name']

            print(f"Results: {track_name}, id: {track_id}")

            track_id_list.append(track_id)   
        except:
            print(response)
            track_id_list.append(np.nan)

    return track_id_list


def get_song_features(songs, track_id):
    ''' Fetches song features for each track_id via Spotify API. Returns a DataFrame.'''

    data = []
    for song,track in zip(songs, track_id):
        print("-"*20)
        print(f"Getting song features for {song}...")

        response = session.get(f"https://api.spotify.com/v1/audio-features/{track}",headers=spotify_headers).json()
        data.append(response)
            

    df = pd.DataFrame(data)

    return df


def main():
    # load in tracks to search on spotify
    tracklist = pd.read_csv('top_100_hip_hop.csv')
    # get track ID for each song
    track_id_list = get_track_ids(tracklist['artist'],tracklist['song'])
    # Append IDs to loaded dataframe.
    tracklist['track_id'] = track_id_list
    # Use track IDs to get song features.
    df = get_song_features(tracklist['song'],tracklist['track_id'])
    # Inner join features on track list.
    merged = tracklist.merge(df, how="inner", left_on='track_id',right_on='id').drop_duplicates("track_id").reset_index(drop=True)
    # Save the new dataframe as a new CSV.
    merged.to_csv("top_100_hip_hop_.csv",index=False)

if __name__=="__main__":
    main()