import argparse
import requests
import sys
from bs4 import BeautifulSoup
from applemusicpy import AppleMusic
import pprint
from settings import *

"""
Name:Pitchfork Best Of
Key ID:4D2ZKVVFJ6
Services:MusicKit
"""

class PitchforkAppleMusic(object):

    def __init__(self, cache_file=None):
        print("Pitchfork to Apple Music")
        self.cache_file = cache_file

    def getSongs(self):
        text = None
        if not self.cache_file:
            url = 'https://pitchfork.com/features/lists-and-guides/the-200-best-songs-of-the-2010s/'
            r = requests.get(url)

            with open('debug.html', 'w') as file:
                file.write(r.text)

            text = r.text
        else:
            with open(self.cache_file, 'r') as file:
                text = file.read()

        soup = BeautifulSoup(text, 'lxml')

        results = [h.contents[0] for h in soup.find_all('h2')]

        songs = []

        for song in results:
            artist_song_split = song.split(':')

            artist = artist_song_split[0]
            song_def = artist_song_split[1]

            stripped_song_def = song_def.strip()[1:]

            just_song = None
            if stripped_song_def.find("”") > -1:
                just_song = stripped_song_def[0:stripped_song_def.index("”")]
            else:
                just_song = stripped_song_def

            year = stripped_song_def[stripped_song_def.rfind('(')+1:stripped_song_def.rfind(')')]

            songs.append({'artist': artist, 'song': just_song, 'year': year})

        return songs


def main():
    secret_key = None

    with open(SECRET_KEY_FILE, 'r') as f:
        secret_key = f.read()

    parser = argparse.ArgumentParser(prog='pitchfork_apple_music')

    parser.add_argument(
        "--get_songs",
        dest="get_songs",
        action="store_true"
    )

    parser.add_argument(
        "--cache_file",
        dest="cache_file"
    )

    args = parser.parse_args()

    cache_file = args.cache_file or None

    am = AppleMusic(secret_key=secret_key, key_id=KEY_ID, team_id=TEAM_ID)
    # results = am.search('Dancing on My Own', types=['songs'], limit=5)
    # for item in results['results']['albums']['data']:
    #     print(item['attributes']['name'])
    if args.get_songs:
        pitchforkAppleMusic = PitchforkAppleMusic(cache_file=cache_file)
        songs = pitchforkAppleMusic.getSongs()

        for song in songs:
            song_results = am.search(song['song'], types=['songs'], limit=5)

            url = ""

            if 'songs' in song_results['results']:
                for item in song_results['results']['songs']['data']:
                    if item['attributes']['artistName'] == song['artist']:
                        url = item['attributes']['url']

                print("Song: " + song['song'] + ", Artist: " + song['artist'] + ", URL: " + url)

if __name__ == '__main__':
    main()