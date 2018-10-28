"""This module does blah blah."""
import MySQLdb

from json import dumps
from bottle import request, response, post, get, put, delete, HTTPResponse
from video import video_repository
from playlist import playlist_repository


@post('/videos/<playlist_id>/<title>/<thumbnail>')
def create_video(playlist_id, title, thumbnail, db):
    playlist = playlist_repository.retrieve_playlist_by_id(playlist_id, db)
    if (playlist == None):
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not add a video to the playlist. It does not exist'})

    position = playlist['video_position'] + 1
    playlist_repository.update_playlist_video_position(
        playlist_id, position, db)
    video_repository.create_video(
        playlist_id, title, thumbnail, position, db)
    return HTTPResponse(status=200, body={'status': 'OK'})


@get('/videos/<playlist_id>')
def retrieve_videos(playlist_id, db):
    rows = video_repository.retrieve_videos(playlist_id, db)
    return HTTPResponse(
        status=200,
        body={'status': 'OK', 'data': rows})


@put('/videos/<id>/<next_position>')
def update_video_position(id, next_position, db):
    video = video_repository.retrieve_video(id, db)
    video_repository.update_video_position(id, video['position'], next_position, db)
    return HTTPResponse(status=200, body={'status': 'OK'})


@delete('/videos/<id>/<playlist_id>')
def delete_video(id, playlist_id, db):
    playlist = playlist_repository.retrieve_playlist_by_id(playlist_id, db)
    if (playlist == None):
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not delete this. It does not exist'})

    video = video_repository.retrieve_video(id, db)

    if (video == None):
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not delete this. this video is not part of this playlist'})

    position = playlist['video_position'] - 1
    playlist_repository.update_playlist_video_position(
        playlist_id, position, db)
    video_repository.delete_video(id, db)
    video_repository.update_video_positions(video['position'], db)
    return HTTPResponse(status=200, body={'status': 'OK'})
