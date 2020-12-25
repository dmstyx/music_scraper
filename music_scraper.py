from bs4 import BeautifulSoup
import requests
import music_database
import re
import random
import urllib.request
import webbrowser
from pprint import pprint


MENU_PROMPT = """Enter:
URL to add albums/songs
Number out of 5 for rating
All to view entire db
Delete to clear db
Find to search db
Play to play random song
Rating to show albums by rating
Exit to quit
\n
"""


def menu():
    try:
        connection = music_database.connect()
    except:
        print("DB conneection failed")
    music_database.create_tables(connection)
    while (user_input := input(MENU_PROMPT)) != "exit":
        if len(user_input) > 7:
            get_music(connection, user_input)
        elif user_input in ["0", "1", "2", "3", "4", "5"]:
            print(int(user_input))
        elif user_input == "all":
            see_all_music(connection)
        elif user_input == "delete":
            delete_db(connection)
        elif user_input == "find":
            get_music_by_artist(connection, user_input)
        elif user_input == "play":
            play_music(connection)
        elif user_input == "rating":
            get_music_by_rating(connection)
            

def get_music(connection, user_input):
    result = requests.get(user_input)

    source = result.content
    soup = BeautifulSoup(source, 'lxml')
    links = soup.find_all('meta', itemprop="name")

    albums = {}

    try:
        find_year = re.search(r'[2]\d{3}', user_input)
        year = find_year.group()
        print(year)
    except:
        year = 0000

    for link in links:
        record = link.attrs['content']
        try:
            album, artist = record.split('-')
            album = album.strip()
            artist = artist.strip()
            albums[artist] = album
            music_database.add_music(connection, artist, album, year)
        except:
            print(f"{record} Not added to list")


def get_music_by_artist(connection, user_input):
    artist = input()
    names = music_database.get_music_by_artist(connection, artist,)

    for name in names:
        print(f"{name[1]} {name[2]} - {name[3]}")


def add_rating(connection, id):
    played = 0
    rating = int(input("Rate album: "))
    music_database.add_rating(connection, rating, played, id)


def play_music(connection):
    num = music_database.count_entries(connection)
    print()
    rand_num = random.randint(1, num[0] + 1)
    ids = music_database.get_music_by_id(connection, rand_num,)
    for id in ids:
        record = f"{id[0]} {id[1]} {id[2]}"
        print(f"Now playing : {record}")

        if id[3] > 0:
            play_music(connection)
        else:
            search = f"{id[1]} {id[2]}"
            search_keyword = search.replace(" ", "")
            try:
                html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                webbrowser.get("firefox").open("https://www.youtube.com/watch?v=" + video_ids[0])
            except:
                print(f"{search_keyword} can't be played")
                play_music(connection)
    add_rating(connection, rand_num)
   

def see_all_music(connection):
    try:
        music = music_database.get_all_music(connection)
        if music == []:
            print("No music available")
        else:
            pprint(music)
    except:
        print("No music available")


def delete_db(connection):
    music_database.delete_tables(connection)


def get_music_by_rating(connection):
    rate = input("Enter minimum rating:")
    names = music_database.get_music_by_rating(connection, rate)

    for name in names:
        print(f"{name[1]} {name[2]} - {name[3]} {name[4]} {name[5]}")


# Play song without clicking on Youtube
# Tidy code
# Add comments
# Error for ratingplay

menu()