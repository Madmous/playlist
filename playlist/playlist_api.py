"""This module does blah blah."""

from bottle import request, response, post, get, put, delete, HTTPResponse
from playlist import playlist_repository
from video import video_repository

from logging import getLogger
logger = getLogger()


@get('/playlists')
def retrieve_playlist(db):
    rows = playlist_repository.retrieve_playlists(db)
    return HTTPResponse(
        status=200,
        body={'status': 'OK', 'data': rows})


@get('/playlists/<id>')
def retrieve_playlist_by_id(id, db):
    row = playlist_repository.retrieve_playlist_by_id(id, db)
    return HTTPResponse(
        status=200,
        body={'status': 'OK', 'data': row})


@post('/playlists/<name>')
def create_playlist(name, db):
    playlist_repository.create_playlist(name, db)
    return HTTPResponse(status=200, body={'status': 'OK'})


@put('/playlists/<id>/<name>')
def update_playlist(id, name, db):
    row = playlist_repository.retrieve_playlist_by_id(id, db)
    if (row == None):
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not update this playlist. It does not exist'})

    playlist_repository.update_playlist(id, name, db)
    return HTTPResponse(status=200, body={'status': 'OK'})


@delete('/playlists/<id>')
def delete_playlist(id, db):
    row = playlist_repository.retrieve_playlist_by_id(id, db)
    if (row == None):
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not delete this playlist. It does not exist'})

    playlist_repository.delete_playlist(id, db)
    video_repository.delete_playlists_videos(id, db)
    return HTTPResponse(status=200, body={'status': 'OK'})
