# Requirements

- MySQL
- Miniconda

# Installation

- conda create -n playlist
- pip install -r requirements.txt

# Run tests

- mysql.server start
- USER='fill in your db user' PASSWORD='fill in your db password' py.test main_test.py

# Start API server

- mysql.server start
- USER='fill in your db user' PASSWORD='fill in your db password' python main.py

When the api server starts, it creates a database called daily_motion and two tables (playlist and video).

## Playlist

### Create a playlist

```bash
curl -X POST \http://localhost:8080/playlists/first%20playlist
```

### Update a playlist

```bash
curl -X PUT \http://localhost:8080/playlists/1/first
```

### Return the list of all playlists

```bash
curl -X GET \http://localhost:8080/playlists
```

### Return one playlist

```bash
curl -X GET \http://localhost:8080/playlists/1
```

### Delete a playlist

```bash
curl -X DELETE \http://localhost:8080/playlists/1
```

### Add a video to a playlist

```bash
curl -X POST \http://localhost:8080/videos/1/title/thumbnail
```

## Video

### Update a video position

```bash
curl -X PUT \http://localhost:8080/videos/1/1/2
```

### Return the list of all videos

```bash
curl -X GET \http://localhost:8080/videos
```

### Return the list of all videos of a playlist

```bash
curl -X GET \http://localhost:8080/videos/1
```

### Delete a video

```bash
curl -X DELETE \http://localhost:8080/videos/1/1
```

# Improvements

- Separate playlists and videos tests into different modules
- Handle database changes like tables changes
- Handle 500 errors due to Database IOs (try catch)
- Authentication
- Query params
- Improve function docstring