
# - Return the list of all videos from a playlist (ordered by position)

# - Add a video in a playlist

# - Delete a video from a playlist
# Removing videos should re-arrange the order of your playlist and the storage.

# evolve model: add playlist id

def retrieve_videos(playlist_id, db):
    db.execute("SELECT id, title, thumbnail from video WHERE playlist_id={playlist_id} ORDER BY position ASC;".format(playlist_id=playlist_id))
    rows = db.fetchall()
    return rows


def delete_video(id, db):
    db.execute("DELETE FROM video where id={id};".format(id=id))


def create_video(playlist_id, title, thumbnail, position, db):
    db.execute(
        "INSERT INTO video (playlist_id, title, thumbnail, position) VALUES({playlist_id}, '{title}', '{thumbnail}', {position});".format(
            playlist_id=playlist_id, title=title, thumbnail=thumbnail, position=position))



