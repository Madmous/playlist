import pytest
import bottle
import webtest
import MySQLdb
import os

from logging import getLogger
from bottle_mysql import Plugin

from video import video_api
from playlist import playlist_api

from database import populate_test_database

logger = getLogger()

app = bottle.default_app()
plugin = Plugin(dbuser='root', dbpass=os.environ["PASSWORD"], dbname='test')
app.install(plugin)
test_app = webtest.TestApp(app)


def create_video(playlist_id, title, thumbnail, position):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO video (playlist_id, title, thumbnail, position) VALUES('{playlist_id}', '{title}', '{thumbnail}', '{position}');".format(
            playlist_id=playlist_id, title=title, thumbnail=thumbnail, position=position))
    db.commit()
    db.close()


def create_playlist(name):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO playlist (name, video_position) VALUES('{name}', 0);".format(name=name))
    db.commit()
    db.close()


def connect_to_database():
    db = MySQLdb.connect("localhost", "root", os.environ["PASSWORD"], 'test')
    return db


def test_should_return_all_playlists():
    populate_test_database()

    create_playlist('first playlist')
    create_playlist('second playlist')

    response = test_app.get('/playlists')
    assert response.status == '200 OK'
    assert response.json['data'] == [dict(id=1, name='first playlist'),
                                     dict(id=2, name='second playlist')]


def test_should_return_a_playlist():
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.get('/playlists/1')
    assert response.status == '200 OK'
    assert response.json['data'] == dict(
        id=1, name='first playlist', video_position=0)


def test_should_create_a_playlist():
    populate_test_database()

    response = test_app.post('/playlists/nn')
    assert response.status == '201 Created'

    response2 = test_app.get('/playlists')
    assert response2.status == '200 OK'
    assert response2.json['data'] == [dict(id=1, name='nn')]


def test_should_update_a_playlist_name():
    populate_test_database()

    response = test_app.post('/playlists/nn')
    assert response.status == '201 Created'

    response2 = test_app.put('/playlists/1/name')
    assert response2.status == '200 OK'

    response3 = test_app.get('/playlists')
    assert response3.json['data'] == [dict(id=1, name='name')]


def test_should_delete_a_playlist_and_remove_all_its_videos():
    populate_test_database()

    create_playlist('first playlist')
    create_video(1, 'the title of the video',
                 'the url of the video', 1)
    create_video(1, 'the title of the video',
                 'the url of the video', 2)

    response = test_app.delete('/playlists/1')
    assert response.status == '200 OK'

    response2 = test_app.get('/playlists/1')
    assert response2.status == '200 OK'
    assert response2.json['data'] == None

    response3 = test_app.get('/videos/1')
    assert response3.status == '200 OK'
    assert response3.json['data'] == []


def test_should_return_all_the_videos():
    populate_test_database()

    create_playlist('first playlist')
    create_video(1, 'the title of the video',
                 'the url of the video', 1)
    create_video(1, 'the title of the video',
                 'the url of the video', 2)

    response = test_app.get('/videos/1')
    assert response.status == '200 OK'
    assert response.json['data'] == [dict(id=1, title='the title of the video',
                                          thumbnail='the url of the video', position=1),
                                     dict(id=2, title='the title of the video',
                                          thumbnail='the url of the video', position=2)]


def test_should_create_a_video():
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.status == '201 Created'

    response = test_app.post('/videos/1/title2/thumbnail2')
    assert response.status == '201 Created'

    response2 = test_app.get('/videos/1')
    assert response2.status == '200 OK'
    assert response2.json['data'] == [dict(id=1, title='title', thumbnail='thumbnail', position=1),
                                      dict(id=2, title='title2', thumbnail='thumbnail2', position=2)]


def test_should_delete_a_video_given_an_id_and_update_playlist_video_position():
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.status == '201 Created'

    response2 = test_app.delete('/videos/1/1')
    assert response2.status == '200 OK'

    response3 = test_app.get('/videos/1')
    assert response3.status == '200 OK'
    assert response3.json['data'] == []

    response4 = test_app.get('/playlists/1')

    assert response4.status == '200 OK'
    assert response4.json['data'] == dict(
        id=1, name='first playlist', video_position=0)


def test_should_reorder_video_position_given_a_deleted_video():
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.status == '201 Created'

    response = test_app.post('/videos/1/title2/thumbnail2')
    assert response.status == '201 Created'

    response = test_app.post('/videos/1/title3/thumbnail3')
    assert response.status == '201 Created'

    deleteResponse = test_app.delete('/videos/2/1')
    assert deleteResponse.status == '200 OK'

    retrieveVideosResponse = test_app.get('/videos/1')
    assert retrieveVideosResponse.status == '200 OK'
    assert retrieveVideosResponse.json['data'] == [dict(id=1, title='title', thumbnail='thumbnail', position=1),
                                                   dict(id=3, title='title3', thumbnail='thumbnail3', position=2)]

    retrievePlaylistResponse = test_app.get('/playlists/1')

    assert retrievePlaylistResponse.status == '200 OK'
    assert retrievePlaylistResponse.json['data'] == dict(
        id=1, name='first playlist', video_position=2)