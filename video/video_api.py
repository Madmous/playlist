"""This module handles video api calls."""
import MySQLdb

from json import dumps
from bottle import request, response, post, get, put, delete, HTTPResponse
from video import video_repository
from playlist import playlist_repository

from logging import getLogger

logger = getLogger()


@post('/videos/<playlist_id>/<title>/<thumbnail>')
def create_video(playlist_id, title, thumbnail, db):
    playlist = playlist_repository.retrieve_playlist_by_id(playlist_id, db)
    if playlist == None:
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not add a video to the playlist. It does not exist'})

    position = playlist['video_position'] + 1
    playlist_repository.update_playlist_video_position(
        playlist_id, position, db)
    video_repository.create_video(
        playlist_id, title, thumbnail, position, db)
    return HTTPResponse(status=200, body={'status': 'OK'})


@get('/videos/<playlist_id>')
def retrieve_videos(playlist_id, db):
    rows = video_repository.retrieve_videos_from_playlist(playlist_id, db)
    return HTTPResponse(
        status=200,
        body={'status': 'OK', 'data': rows})


@get('/videos')
def retrieve_videos(db):
    rows = video_repository.retrieve_videos(db)
    return HTTPResponse(
        status=200,
        body={'status': 'OK', 'data': rows})


@put('/videos/<id>/<playlist_id>/<next_position>')
def update_video_position(id, playlist_id, next_position, db):
    video = video_repository.retrieve_video(id, playlist_id, db)
    if video == None:
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not update this video. It does not exist'})

    last_position = video_repository.retrieve_last_video_position(
        playlist_id, db)
    next_position = int(next_position, base=10)
    if next_position > last_position:
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not update this video. The next position does not exist'})

    position = video['position']
    if next_position == position:
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'There is no need to update this video since the position is already the one specified'})

    if position > next_position:
        video_repository.move_up_video_position(
            id, position, next_position, db)
        return HTTPResponse(status=200, body={'status': 'OK'})

    video_repository.drop_down_video_position(id, position, next_position, db)
    return HTTPResponse(status=200, body={'status': 'OK'})


@delete('/videos/<id>/<playlist_id>')
def delete_video(id, playlist_id, db):
    playlist = playlist_repository.retrieve_playlist_by_id(playlist_id, db)
    if playlist == None:
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not delete this. It does not exist'})

    video = video_repository.retrieve_video(id, playlist_id, db)

    if video == None:
        return HTTPResponse(status=200, body={'status': 'NOK', 'message': 'You can not delete this. this video is not part of this playlist'})

    position = playlist['video_position'] - 1
    playlist_repository.update_playlist_video_position(
        playlist_id, position, db)
    video_repository.delete_video(id, db)
    video_repository.update_video_positions(video['position'], db)
    return HTTPResponse(status=200, body={'status': 'OK'})
