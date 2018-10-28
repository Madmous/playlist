"""This module does blah blah."""
import MySQLdb

from json import dumps
from bottle import request, response, post, get, put, delete, HTTPResponse
from video import video_repository
from playlist import playlist_repository


@post('/videos/<playlist_id>/<title>/<thumbnail>')
def create_video(playlist_id, title, thumbnail, db):
    playlist = playlist_repository.retrieve_playlist_by_id(playlist_id, db)
    position = playlist['video_position'] + 1
    playlist_repository.update_playlist_video_position(
        playlist_id, position, db)
    video_repository.create_video(playlist_id, title, thumbnail, position, db)
    return HTTPResponse(status=201)


@get('/videos/<playlist_id>')
def retrieve_videos(playlist_id, db):
    rows = video_repository.retrieve_videos(playlist_id, db)
    return HTTPResponse(
        status=200,
        body={'data': rows})


@put('/videos/<id>')
def update_video(id):
    pass


@delete('/videos/<id>/<playlist_id>')
def delete_video(id, playlist_id, db):
    playlist = playlist_repository.retrieve_playlist_by_id(playlist_id, db)
    position = playlist['video_position'] - 1
    playlist_repository.update_playlist_video_position(
        playlist_id, position, db)
    video = video_repository.delete_video(id, db)
    video_repository.update_video_positions(video['position'], db)
    return HTTPResponse(status=200)
