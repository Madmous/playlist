"""This module does blah blah."""
# update video position ???

def retrieve_videos(playlist_id, db):
    db.execute("SELECT id, title, thumbnail, position from video WHERE playlist_id={playlist_id} ORDER BY position ASC;".format(
        playlist_id=playlist_id))
    rows = db.fetchall()
    return rows


def retrieve_video_position(id, db):
    db.execute("SELECT id, position from video WHERE id={id};".format(id=id))
    row = db.fetchone()
    return row


def delete_video(id, db):
    db.execute("DELETE FROM video where id={id};".format(id=id))


def delete_playlists_videos(playlist_id, db):
    db.execute("DELETE FROM video where playlist_id={playlist_id};".format(
        playlist_id=playlist_id))


def create_video(playlist_id, title, thumbnail, position, db):
    db.execute(
        "INSERT INTO video (playlist_id, title, thumbnail, position) VALUES({playlist_id}, '{title}', '{thumbnail}', {position});".format(
            playlist_id=playlist_id, title=title, thumbnail=thumbnail, position=position))


def update_video_positions(removed_position, db):
    db.execute("UPDATE video SET position = position - 1 WHERE position > {removed_position}".format(
        removed_position=removed_position))
