
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from spotify_config import spotify_headers
import numpy as np


# In[2]:


# load in tracks to search on spotify
tracklist = pd.read_csv('top_edm_songs.csv')


# In[3]:


tracklist.head()


# In[4]:


def encode_spaces(string_list):
    '''Replaces spaces with %20 for Spotify API search'''
    encoded = [string.replace(" ", "%20") for string in string_list]
    return encoded


# In[5]:


encoded_artist_name = encode_spaces(tracklist['artist'])
encoded_song_name = encode_spaces(tracklist['song'])


# In[6]:


# Tie the strings together to form query
for artist,song in zip(encoded_artist_name,encoded_song_name):
    print(artist+"%20"+song)
    query = artist+"%20"+song
    break

base_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
print(base_url)


# In[7]:


response = requests.get(base_url,headers=spotify_headers).json()


# In[8]:


track_id = response['tracks']['items'][0]['name']
track_id


# In[9]:


def clean_search_terms(string):
    '''Cleans up string for spotify search.'''
    cleaned = string.replace("%20Featuring%20","%20")    .replace("%20X%20","%20")    .replace("%20x%20","%20")    .replace("%20VS%20","%20")    .replace("%20VS%20","%20")    .replace("#","")
    return cleaned


# In[10]:


track_id_list = []

for artist,song in zip(encoded_artist_name,encoded_song_name):
    print("-"*20)
    print("Searching Spotify API for...")
    print(artist.replace("%20"," "), song.replace("%20"," "))
    print("-"*20)

    artist_ = clean_search_terms(artist)
    
    query = artist_+"%20"+song
    base_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
#     print(base_url)
    
    response = requests.get(base_url,headers=spotify_headers).json()
    
    try:
        track_id = response['tracks']['items'][0]['id']
        track_name = response['tracks']['items'][0]['name']

        print(f"Results: {track_name}, id: {track_id}")
        
        track_id_list.append(track_id)   
    except:
        print(response)
        track_id_list.append(np.nan)


# In[20]:


print(track_id_list)


# In[21]:


tracklist['track_id'] = track_id_list
tracklist.head()


# In[22]:


tracklist[tracklist['track_id'].isna()]


# In[27]:


for track in tracklist['track_id']:
    response = requests.get(f"https://api.spotify.com/v1/audio-features/{track}",headers=spotify_headers).json()
    print(track)
    print(response)
    break    


# In[30]:

def get_song_features():
    for song,track in zip(tracklist['song'], tracklist['track_id']):
        danceability, energy, loudness, liveness, tempo = [],[],[],[],[]
        
        response = requests.get(f"https://api.spotify.com/v1/audio-features/{track}",headers=spotify_headers).json()
        
        print("-"*20)
        print(f"Getting song features for {song}...")
        print("-"*20)

        try:
            danceability.append(response['danceability'])
            energy.append(response['energy'])
            loudness.append(response['loudness'])
            liveness.append(response['liveness'])
            tempo.append(response['tempo'])
        except:
            print(response)
            danceability.append(np.nan)
            energy.append(np.nan)
            loudness.append(np.nan)
            liveness.append(np.nan)
            tempo.append(np.nan)
        

