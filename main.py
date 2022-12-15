from spotify_helper import SpotifyHelper
from song_lists import get_songs_100

songs_100 = get_songs_100()
print(songs_100)
my_sp = SpotifyHelper(scope='playlist-modify-private')
song_urls = my_sp.get_song_urls(songs_100)
print(len(song_urls))
p_id = my_sp.make_playlist(unique_playlist_name=songs_100['playlist_name'])
my_sp.add_to_playlist(song_urls=song_urls, playlist_id=p_id)
