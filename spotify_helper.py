import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from app_secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIFY_USER_ID, PLAYLIST_NAME


class SpotifyHelper:
    def __init__(self, scope):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))

    def get_song_urls(self, songs: dict) -> list:
        song_urls = []
        year = songs['year']
        titles_and_artists = songs['songs_100']
        for item in titles_and_artists:
            print('ok')
            data = self.sp.search(
                q=f"track:{item['name']} artist:{item['artist']} year:{year}")
            try:
                song_url = data['tracks']['items'][0]['external_urls']['spotify']
                song_urls.append(song_url)
            except IndexError:
                pass
        return song_urls

    def test(self):
        data = self.sp.search(
            q=f"track:As It Was artist:Harry Styles year:2022")
        song_url = data['tracks']['items'][0]['external_urls']['spotify']
        print(song_url)

    def make_playlist(self, unique_playlist_name):
        try:
            with open('playlists.json', 'r') as f:
                data = json.load(f)
            for item in data:
                if item['name'] == unique_playlist_name:
                    return item['playlist_id']
            playlist = self.sp.user_playlist_create(
                user=SPOTIFY_USER_ID, name=unique_playlist_name, public=False)
            data.append(dict(name=unique_playlist_name,
                        playlist_id=playlist['id']))
            with open('playlists.json', 'w') as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            playlist = self.sp.user_playlist_create(
                user=SPOTIFY_USER_ID, name=unique_playlist_name, public=False)
            data = [dict(name=unique_playlist_name,
                         playlist_id=playlist['id'])]
            with open('playlists.json', 'w') as f:
                json.dump(data, f, indent=4)
            return playlist['id']

    def add_to_playlist(self, song_urls: list, playlist_id):
        self.sp.user_playlist_add_tracks(
            user=SPOTIFY_USER_ID, playlist_id=playlist_id, tracks=song_urls)
