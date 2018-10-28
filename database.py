import os

from MySQLdb import connect


def create_schema_if_necessary(name):
    db = connect_to_mysql()
    cursor = db.cursor()
    create_database(cursor, 'daily_motion')
    create_video_table(cursor)
    create_playlist_table(cursor)
    db.commit()
    db.close()


def populate_test_database():
    db = connect_to_mysql()
    cursor = db.cursor()
    drop_database(cursor, 'test')
    create_database(cursor, 'test')
    create_video_table(cursor)
    create_playlist_table(cursor)
    db.commit()
    db.close()


def connect_to_mysql():
    db = connect("localhost", "root", os.environ["PASSWORD"])
    return db


def create_database(cursor, name):
    cursor.execute("CREATE DATABASE IF NOT EXISTS {name};".format(name=name))
    cursor.execute("USE {name};".format(name=name))


def create_video_table(cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS video(id int NOT NULL AUTO_INCREMENT, playlist_id int NOT NULL, title varchar(50) NOT NULL, thumbnail varchar(50) NOT NULL, position int NOT NULL, created DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id));")


def create_playlist_table(cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS playlist(id int NOT NULL AUTO_INCREMENT, name varchar(50) NOT NULL, video_position int, created DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id));")


def drop_database(cursor, name):
    cursor.execute("DROP DATABASE IF EXISTS {name};".format(name=name))
