import sqlite3


CREATE_MUSIC_TABLE = "CREATE TABLE IF NOT EXISTS music (id INTEGER PRIMARY KEY, artist TEXT, album TEXT, played INTEGER DEFAULT 0.00,year INTEGER,rating INTEGER DEFAULT 0.00);"
INSERT_MUSIC = "INSERT INTO music (artist, album, year) VALUES(?, ?, ?);"

GET_ALL_MUSIC = "SELECT * FROM music;"

GET_MUSIC_BY_ALBUM = "SELECT * FROM music WHERE album = ?;"

GET_MUSIC_BY_ARTIST ="""
SELECT * FROM music
WHERE artist = ?
ORDER BY rating DESC
LIMIT 1;"""

GET_MUSIC_BY_ID ="""
SELECT * FROM music
WHERE id = ?
ORDER BY rating DESC
LIMIT 1;"""

DELETE_TABLE = "DROP TABLE IF EXISTS music;"

COUNT_ENTRIES = "SELECT COUNT(*) FROM music;"

UPDATE_RATING = "UPDATE music SET rating = ?, played = ? WHERE id = ?;"

GET_MUSIC_BY_RATING = "SELECT * FROM music WHERE rating > ?;"


def connect():
    return sqlite3.connect("data.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_MUSIC_TABLE)


def add_music(connection, artist, album, year):
    with connection:
        connection.execute(INSERT_MUSIC, (artist, album, year))


def get_all_music(connection):
    with connection:
        return connection.execute(GET_ALL_MUSIC).fetchall()


def get_music_by_artist(connection, artist):
    with connection:
        return connection.execute(GET_MUSIC_BY_ARTIST, (artist,)).fetchall()


def get_music_by_id(connection, id):
    with connection:
        return connection.execute(GET_MUSIC_BY_ID, (id,)).fetchall()


def delete_tables(connection):
    with connection:
        connection.execute(DELETE_TABLE)


def count_entries(connection):
    with connection:
        number = connection.execute(COUNT_ENTRIES)
        num = number.fetchone()
        return num


def add_rating(connection, rating, played, id):
    with connection:
        played += 1
        connection.execute(UPDATE_RATING, (rating, played, id,))


def get_music_by_rating(connection, rating):
    with connection:
        return connection.execute(GET_MUSIC_BY_RATING, (rating,)).fetchall()