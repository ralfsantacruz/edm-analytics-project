# import base64
import requests as rq
# Access Key for Spotify

# spotify_client_data = base64.b64encode(b"c6a240ff49a14773aaeb597b589db15d:187a6669e12046669de64d01bbc8439c")

spotify_client_data = "YzZhMjQwZmY0OWExNDc3M2FhZWI1OTdiNTg5ZGIxNWQ6MTg3YTY2NjllMTIwNDY2NjlkZTY0ZDAxYmJjODQzOWM="

# Create post request to get access token to spotify.
headers = {'Authorization': 'Basic '+ spotify_client_data}
payload = {'grant_type': 'client_credentials'}

response = rq.post("https://accounts.spotify.com/api/token", headers=headers,data=payload).json()

# Save access token
token = response['access_token']

# Set authorization header using token
spotify_headers = {'Authorization': 'Bearer ' + token}

