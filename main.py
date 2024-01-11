import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
from bs4 import BeautifulSoup
URL = "https://www.billboard.com/charts/hot-100/1991-04-06/"
SPOTIFY_ID = os.environ["SPOT_ID"]
SPOTIFY_AUTH = os.environ["SPOT_AUTH"]
date = input(" Which year you would like to travel to? Type the date in this format YYY-MM-DD:  ")

website = requests.get(url=URL)
website_view = website.text
# print(website_view)

# scoop with beautiful soup
soup = BeautifulSoup(website_view, "html.parser")
# print(soup.prettify())

# capture the link with all details
full_detail = soup.select("li ul li h3")
artist = [name.getText().strip() for name in full_detail]
print(artist)

"""STEP 2, AUTHENTICATION WITH SPOTIFY"""

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:4304/auth/spotify/callback",
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_AUTH,
        show_dialog=True,
        cache_path="token.txt",
        username="Danielcodes",

    )
)

user_id = sp.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in artist:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


