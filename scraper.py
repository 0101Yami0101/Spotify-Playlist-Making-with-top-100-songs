#Songs scraper and Spotify Api

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

date = input("Enter Date in (yyyy-mm-dd) format: ")

hot100URL = "https://www.billboard.com/charts/hot-100/2000-01-01/"
response = requests.get(url = hot100URL)
data = response.text
soup = BeautifulSoup(data, "html.parser")

#dataLists
songsList = []
title_data = soup.select(selector= "div li ul li h3")

for titleTag in title_data:
    text = titleTag.getText().strip()
    songsList.append(text)

#Spotify

Client_ID = "YOUR ID"   
Client_Secret = "YOUR SECRET"
URI = "http://example.com"
scope = "playlist-modify-private"

#authorisation code flow
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= Client_ID, client_secret= Client_Secret,redirect_uri= URI ,scope=scope)) #Access token generated in cache after successful execution

#get current authenticated user data
result_dict = sp.current_user()
user_ID = result_dict["id"]

#Searching for tracks and creating URI list
year = date.split("-")[0]
song_URI_list = []

for song in songsList:
    query = f"track: {song} year: {year}"
    search_resp = sp.search(q= query)

    try:
        uri = search_resp["tracks"]["items"][0]["uri"]
        song_URI_list.append(uri)
    except IndexError:
        print(f"The song named - {song} is not available in spotify. Skipped")

# print(song_URI_list)   

#create private playlist on the user account named "YYYY-MM-DD Billboard 100"
playlist_nm = f"{date}- Billboard 100"
playlist_ID = sp.user_playlist_create(user= user_ID, name= playlist_nm,public= False)["id"] #creating playlist and getting playlist ID

sp.playlist_add_items(playlist_id= playlist_ID, items= song_URI_list) #adding tracks using URI list to newly created playlist



        


