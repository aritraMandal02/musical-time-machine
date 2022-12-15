import requests
from bs4 import BeautifulSoup


def get_songs_100():
    date = input(
        'Which year do you want to travel to? Type date in this format YYYY-MM-DD: ')
    url = f'https://www.billboard.com/charts/hot-100/{date}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    songs_100 = [dict(name=song.find(id='title-of-a-story').getText().strip(),
                      artist=song.find_all(name='span')[1].getText().strip())
                 for song in soup.find_all(class_='o-chart-results-list-row-container')]
    hundred_songs_playlist = dict(
        playlist_name=f'Songs on {date}', year=date.split('-')[0], songs_100=songs_100)
    return hundred_songs_playlist
