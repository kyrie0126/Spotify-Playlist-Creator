from bs4 import BeautifulSoup
import requests
import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy


# ----------------------------------------- User Prompt -----------------------------------------
date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD\n")
year = date[0:4]


# ----------------------------------------- Billboard Website Scraping -----------------------------------------
url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url)
content = response.text

soup = BeautifulSoup(content, 'html.parser')
song_search = soup.find_all(name='div', class_='o-chart-results-list-row-container')

song_list = []
for song in song_search:
    title = song.find(name='h3', id='title-of-a-story')
    title2 = title.getText()
    title3 = title2.replace("\n", "")
    title4 = title3.replace("\t", "")
    song_list.append(title4)
print(song_list)


# ----------------------------------------- Spotify API -----------------------------------------
# create spotify instance - need run line 35 then re-open project for token.txt to be available
# note: I have client_id and client_secret saved as environment variables
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ['SPOTIPY_CLIENT_ID'],
        client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
        redirect_uri='http://example.com',
        scope='playlist-modify-private',
        show_dialog=True,
        cache_path='token.txt'
    )
)

# retrieve username
sp_username = sp.current_user()['id']

# retrieve URIs for songs in song_list
uri_list = []
for song in song_list:
    try:
        track = sp.search(
            q=f'track: {song} year: {year}',
            type='track'
        )
        uri_list.append(track['tracks']['items'][0]['uri'])
    except IndexError:
        pass

# create playlist in spotify
pl = sp.user_playlist_create(
    user=sp_username,
    name=f"Billboard's Top 100 from {date}",
    public=False
)

# add top 100 songs by URI
sp.playlist_add_items(
    playlist_id=pl['id'],
    items=uri_list
)
