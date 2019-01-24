import pandas as pd
import numpy as np

import os

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

############### Search Formatting Functions ###############
def encode_spaces(string_list):
    '''Replaces spaces with %20 for Spotify API search.'''
    encoded = [string.replace(" ", "%20") for string in string_list]
    return encoded


def clean_search_terms(string):
    '''Cleans up string for spotify search.'''
    cleaned = string.replace("%20Featuring%20","%20").replace("%20X%20","%20").replace("%20x%20","%20").replace("%20VS%20","%20").replace("%20VS%20","%20").replace("#","")
    return cleaned


############### Data Fetching Functions ###############

def get_track_ids(artists, songs):

    '''
    Returns a list of track IDs for songs. Takes in two lists or series as arguments.
    Artist and Song are plugged into Spotify Search to return IDs. 
    '''

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
            

    df = pd.DataFrame(data).drop(columns= 'error')

    return df


def make_ranks(df):
    '''
    Makes ranks for each artist according to year. Natural order of rows comes from Billboard's ranking.
    Appends number according to row order by year.
    '''
    rank=[]

    # Create ranks for each artist.
    for year in sorted(list(set(df['year']))):
        rank+=[i+1 for i in range(len(df[df['year']==year]))]
    return rank


############### Consolidation Function ###############

def append_features(genre):

    '''Returns a merged dataframe with songs, artists, and Spotify track features.'''

    # Load in tracks to search on spotify.
    tracklist = pd.read_csv(f'top_100_{genre}.csv')
    # Get track ID for each song.
    track_id_list = get_track_ids(tracklist['artist'],tracklist['song'])

    # Append IDs to loaded dataframe.
    tracklist['track_id'] = track_id_list
    tracklist['rank'] = make_ranks(tracklist)

    # Use track IDs to get song features and save as dataframe.
    df = get_song_features(tracklist['song'],tracklist['track_id'])

    # Inner join features on track IDs.
    print('Merging dataframes...')    
    merged_df = tracklist.merge(df, how="inner", left_on='track_id',right_on='id').drop_duplicates("track_id").reset_index(drop=True)

    # Save the new dataframe as a new CSV as backup.
    merged_df.to_csv(
        os.path.join(f"db_backup/top_100_{genre}_.csv"),
        index=False
        )

    # Remove the old CSV.
    os.remove(f'top_100_{genre}.csv')

    return merged_df




# def main():
#     # Set up requests session and to account for retries should connection errors arise.
#     session = requests.Session()
#     retry = Retry(connect=3, backoff_factor=0.5)
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)

#     # load in tracks to search on spotify.
#     tracklist = pd.read_csv('top_100_hip_hop.csv')
#     # get track ID for each song.
#     track_id_list = get_track_ids(tracklist['artist'],tracklist['song'])

#     # Append IDs to loaded dataframe.
#     tracklist['track_id'] = track_id_list
#     tracklist['rank'] = make_ranks(tracklist)

#     # Use track IDs to get song features and save as dataframe.
#     df = get_song_features(tracklist['song'],tracklist['track_id'])

#     # Inner join features on track IDs.
#     merged = tracklist.merge(df, how="inner", left_on='track_id',right_on='id').drop_duplicates("track_id").reset_index(drop=True)

#     # Save the new dataframe as a new CSV.
#     merged.to_csv("top_100_hip_hop_.csv",index=False)

# if __name__=="__main__":
#     main()

