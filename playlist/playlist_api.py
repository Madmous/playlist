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
        body={'data': rows})


@get('/playlists/<id>')
def retrieve_playlist_by_id(id, db):
    rows = playlist_repository.retrieve_playlist_by_id(id, db)
    return HTTPResponse(
        status=200,
        body={'data': rows})


@post('/playlists/<name>')
def create_playlist(name, db):
    playlist_repository.create_playlist(name, db)
    return HTTPResponse(status=201)


@put('/playlists/<id>/<name>')
def update_playlist(id, name, db):
    playlist_repository.update_playlist(id, name, db)
    return HTTPResponse(status=200)


@delete('/playlists/<id>')
def delete_playlist(id, db):
    playlist_repository.delete_playlist(id, db)
    video_repository.delete_playlists_videos(id, db)
    return HTTPResponse(status=200)
