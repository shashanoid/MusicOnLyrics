#!/usr/bin/python

from __future__ import print_function
import os
import re

from bs4 import BeautifulSoup

# Version compatiblity
import sys
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib2 import urlopen
    from urllib import quote_plus as qp


def extract_videos(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]


def list_movies(movies):
    for idx, (title, _) in enumerate(movies):
        yield '[{}] {}'.format(idx, title)


def search_videos(query):
    response = urlopen('https://www.youtube.com/results?search_query=' + query)
    return extract_videos(response.read())


def main():
   
    search = ''
    while search.strip() == '':
        search = raw_input('Enter songname/lyrics/artist or other\n> ')
    search = qp(search)

    print('Searching...')
    available = search_videos(search)

    if not available:
        print('No results found matching your query.')
        sys.exit()

    print("Found:", '\n', '\n'.join(list_movies(available)))
    print ('-----------------------------------------------------------------')

    print('\n')

    choice = ''
    while choice.strip() == '':
        choice = raw_input('Pick one: ')

    title, video_link = available[int(choice)]

    prompt = raw_input("Download (y/n)? ")
    if prompt != "y":
        sys.exit()

    command_tokens = [
        'youtube-dl',
        '--extract-audio',
        '--audio-format mp3',
        '--audio-quality 0',
        'http://www.youtube.com/' + video_link]

    command = ' '.join(command_tokens)

    print('Downloading...')
    os.system(command)

if __name__ == '__main__':
    main()