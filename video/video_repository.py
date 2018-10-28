"""This module is the video repository in charge of all database requests."""


def retrieve_videos_from_playlist(playlist_id, db):
    db.execute("SELECT id, title, thumbnail, position from video WHERE playlist_id=%s ORDER BY position ASC;", (playlist_id,))
    rows = db.fetchall()
    return rows


def retrieve_videos(db):
    db.execute(
        "SELECT id, playlist_id, title, thumbnail, position from video ORDER BY playlist_id ASC, position ASC;")
    rows = db.fetchall()
    return rows


def retrieve_video(id, playlist_id, db):
    db.execute(
        "SELECT id, position from video WHERE id=%s and playlist_id=%s;", (id, playlist_id))
    row = db.fetchone()
    return row


def retrieve_last_video_position(playlist_id, db):
    db.execute(
        "SELECT max(position) as position from video WHERE playlist_id=%s;", (playlist_id,))
    row = db.fetchone()
    return row['position']


def delete_video(id, db):
    db.execute("DELETE FROM video where id=%s;", (id,))


def delete_playlists_videos(playlist_id, db):
    db.execute("DELETE FROM video where playlist_id=%s;", (playlist_id,))


def create_video(playlist_id, title, thumbnail, position, db):
    db.execute("INSERT INTO video (playlist_id, title, thumbnail, position) VALUES(%s, %s, %s, %s);",
               (playlist_id, title, thumbnail, position))


def update_video_positions(removed_position, db):
    db.execute("UPDATE video SET position = position - 1 WHERE position > %s", (removed_position,))


def update_video_position(id, position, next_position, db):
    db.execute("UPDATE video SET position = Case position When %s Then %s Else position + 1 End WHERE position BETWEEN %s AND %s;", (position, next_position, next_position, position))
