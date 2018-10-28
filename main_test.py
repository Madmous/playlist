import os
import MySQLdb
import webtest

from bottle_mysql import Plugin
import bottle

from video import video_api
from playlist import playlist_api

from database import populate_test_database

app = bottle.default_app()
plugin = Plugin(
    dbuser=os.environ["USER"], dbpass=os.environ["PASSWORD"], dbname=os.environ["DB"])
app.install(plugin)
test_app = webtest.TestApp(app)


def create_video(playlist_id, title, thumbnail, position):
    """Connect to database and create video table"""
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("INSERT INTO video (playlist_id, title, thumbnail, position) VALUES(%s, %s, %s, %s);",
                   (playlist_id, title, thumbnail, position,))
    db.commit()
    db.close()


def create_playlist(name):
    """Connect to database and create playlsit table"""
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO playlist (name, video_position) VALUES(%s, 0);", (name,))
    db.commit()
    db.close()


def connect_to_database():
    """Connect to database"""
    database = MySQLdb.connect(
        "localhost", os.environ["USER"], os.environ["PASSWORD"], os.environ["DB"])
    return database


def test_playlists():
    """should return all playlists"""
    populate_test_database()

    create_playlist('first playlist')
    create_playlist('second playlist')

    response = test_app.get('/playlists')
    assert response.json['status'] == 'OK'
    assert response.json['data'] == [dict(id=1, name='first playlist'),
                                     dict(id=2, name='second playlist')]


def test_playlist():
    """should return playlist"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.get('/playlists/1')
    assert response.json['status'] == 'OK'
    assert response.json['data'] == dict(
        id=1, name='first playlist', video_position=0)


def test_create_a_playlist():
    """should create playlist given a name"""
    populate_test_database()

    response = test_app.post('/playlists/nn')
    assert response.json['status'] == 'OK'

    response2 = test_app.get('/playlists')
    assert response2.json['status'] == 'OK'
    assert response2.json['data'] == [dict(id=1, name='nn')]


def test_update_playlist():
    """should update a playlist name"""
    populate_test_database()

    response = test_app.post('/playlists/nn')
    assert response.json['status'] == 'OK'

    response2 = test_app.put('/playlists/1/name')
    assert response2.json['status'] == 'OK'

    response3 = test_app.get('/playlists')
    assert response3.json['status'] == 'OK'
    assert response3.json['data'] == [dict(id=1, name='name')]


def test_delete_playlist():
    """should delete a playlist and all its videos given an id"""
    populate_test_database()

    create_playlist('first playlist')
    create_video(1, 'the title of the video',
                 'the url of the video', 1)
    create_video(1, 'the title of the video',
                 'the url of the video', 2)

    response = test_app.delete('/playlists/1')
    assert response.json['status'] == 'OK'

    response2 = test_app.get('/playlists/1')
    assert response2.json['status'] == 'OK'
    assert response2.json['data'] is None

    response3 = test_app.get('/videos/1')
    assert response3.json['status'] == 'OK'
    assert response3.json['data'] == []


def test_the_platlist_videos():
    """should return all videos from a playlist"""
    populate_test_database()

    create_playlist('first playlist')
    create_video(1, 'the title of the video',
                 'the url of the video', 1)
    create_video(1, 'the title of the video',
                 'the url of the video', 2)

    response = test_app.get('/videos/1')
    assert response.json['status'] == 'OK'
    assert response.json['data'] == [dict(id=1, title='the title of the video',
                                          thumbnail='the url of the video', position=1),
                                     dict(id=2, title='the title of the video',
                                          thumbnail='the url of the video', position=2)]


def test_videos():
    """should return all the videos"""
    populate_test_database()

    create_playlist('first playlist')
    create_playlist('second playlist')
    create_video(1, 'f title',
                 'f url', 1)
    create_video(1, 's title',
                 's url', 2)
    create_video(1, 't title',
                 't url', 3)
    create_video(2, 'f title',
                 'f url', 1)
    create_video(2, 'fh title',
                 'fh url', 2)

    response = test_app.get('/videos')
    assert response.json['status'] == 'OK'
    assert response.json['data'] == [
        dict(id=1, playlist_id=1, title='f title',
             thumbnail='f url', position=1),
        dict(id=2, playlist_id=1, title='s title',
             thumbnail='s url', position=2),
        dict(id=3, playlist_id=1, title='t title',
             thumbnail='t url', position=3),
        dict(id=4, playlist_id=2, title='f title',
             thumbnail='f url', position=1),
        dict(id=5, playlist_id=2, title='fh title',
             thumbnail='fh url', position=2)
    ]


def test_create_video():
    """should create a playlist video"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.json['status'] == 'OK'

    response2 = test_app.post('/videos/1/title2/thumbnail2')
    assert response2.json['status'] == 'OK'

    response3 = test_app.get('/videos/1')
    assert response3.json['status'] == 'OK'
    assert response3.json['data'] == [
        dict(id=1, title='title', thumbnail='thumbnail', position=1),
        dict(id=2, title='title2', thumbnail='thumbnail2', position=2)
    ]


def test_drop_down_a_video_position():
    """should update a video position when it has to drop down"""
    populate_test_database()

    create_playlist('first playlist')

    create_video(1, 'title', 'thumbnail', 1)
    create_video(1, 'title2', 'thumbnail2', 2)

    response = test_app.put('/videos/1/1/2')
    assert response.json['status'] == 'OK'

    response2 = test_app.get('/videos/1')
    assert response2.json['status'] == 'OK'
    assert response2.json['data'] == [
        dict(id=2, title='title2', thumbnail='thumbnail2', position=1),
        dict(id=1, title='title', thumbnail='thumbnail', position=2)
    ]


def test_move_up_a_video_position():
    """should update a video position when it has to move up"""
    populate_test_database()

    create_playlist('first playlist')

    create_video(1, 'title', 'thumbnail', 1)
    create_video(1, 'title2', 'thumbnail2', 2)

    response = test_app.put('/videos/2/1/1')
    assert response.json['status'] == 'OK'

    response2 = test_app.get('/videos/1')
    assert response2.json['status'] == 'OK'
    assert response2.json['data'] == [
        dict(id=2, title='title2', thumbnail='thumbnail2', position=1),
        dict(id=1, title='title', thumbnail='thumbnail', position=2)
    ]


def test_delete_video():
    """should delete a video position given an id and update the platlist video position it has to drop down"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.json['status'] == 'OK'

    response2 = test_app.delete('/videos/1/1')
    assert response2.json['status'] == 'OK'

    response3 = test_app.get('/videos/1')
    assert response3.json['status'] == 'OK'
    assert response3.json['data'] == []

    response4 = test_app.get('/playlists/1')

    assert response4.json['status'] == 'OK'
    assert response4.json['data'] == dict(
        id=1, name='first playlist', video_position=0)


def test_reorder_video_positions():
    """should reorder all video positions when a video is deleted"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.json['status'] == 'OK'

    response2 = test_app.post('/videos/1/title2/thumbnail2')
    assert response2.json['status'] == 'OK'

    response3 = test_app.post('/videos/1/title3/thumbnail3')
    assert response3.json['status'] == 'OK'

    response4 = test_app.delete('/videos/2/1')
    assert response4.json['status'] == 'OK'

    response5 = test_app.get('/videos/1')
    assert response.json['status'] == 'OK'
    assert response5.json['data'] == [
        dict(id=1, title='title', thumbnail='thumbnail', position=1),
        dict(id=3, title='title3', thumbnail='thumbnail3', position=2)
    ]

    response6 = test_app.get('/playlists/1')
    assert response6.json['status'] == 'OK'
    assert response6.json['data'] == dict(
        id=1, name='first playlist', video_position=2)


def test_delete_playlist_with_unkwnown_id():
    """should have a NOK status when deleting an unknown playlist id"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.delete('/playlists/2')
    assert response.json['status'] == 'NOK'
    assert response.json['message'] is not None


def test_update_playlist_with_unknown_id():
    """should have a NOK status when updating an unknown playlist id"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.put('/playlists/2/name')
    assert response.json['status'] == 'NOK'
    assert response.json['message'] is not None


def test_create_video_with_unknown_playlist_id():
    """should have a NOK status when creating a video with an unknown playlist id"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/2/title/thumbnail')

    assert response.json['status'] == 'NOK'
    assert response.json['message'] is not None


def test_update_video_with_unknown_playlist_id():
    """should have a NOK status when updating a video with an unknown playlist id"""
    populate_test_database()

    response = test_app.put('/videos/1/1/2')
    assert response.json['status'] == 'NOK'
    assert response.json['message'] is not None


def test_update_video_with_out_of_bounds_position():
    """should have a NOK status when updating a video with an out of bounds position"""
    populate_test_database()

    create_video(1, 'title', 'thumbnail', 1)
    create_video(1, 'title2', 'thumbnail2', 2)

    response = test_app.put('/videos/2/1/2')
    assert response.json['status'] == 'NOK'
    assert response.json['message'] is not None

    response2 = test_app.put('/videos/1/1/5')
    assert response2.json['status'] == 'NOK'
    assert response2.json['message'] is not None


def test_delete_video_with_an_unknown_playlist_id():
    """should have a NOK status when deleting a video with an unknown playlist id"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.json['status'] == 'OK'

    response = test_app.delete('/videos/1/2')
    assert response.json['status'] == 'NOK'
    assert response.json['message'] is not None


def test_delete_video_with_an_unknown_id():
    """should have a NOK status when deleting an unknown video id"""
    populate_test_database()

    create_playlist('first playlist')

    response = test_app.post('/videos/1/title/thumbnail')
    assert response.json['status'] == 'OK'

    response = test_app.delete('/videos/2/1')
    assert response.json['status'] == 'NOK'
    assert response.json['message'] is not None
