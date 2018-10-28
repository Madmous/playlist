Building a playlist api
Indicative estimated duration : 3h00

Introduction

Dailymotion is building a new feature "The playlist"

The feature is simple : The user can create a list of ordered videos.

As a core api developer, you are responsible for building this feature and expose it through API.

Task
The task is to create an api that manages an ordered playlist.
An example of a minimal video model : (You might add extra fields to do this project)

video {
id : the id of the video,
title: the title of the video
thumbnail : The url of the video
...
}

An example of a minimal playlist model : (You might add extra fields to do this project)

playlist {
id : The id of the playlist,
name : The name of the playlist
......
}

The API must support the following use cases:

- Return the list of all videos:

{
"data" : [
{
"id": 1,
"title": "video 1"
....
},
{
"id": 2,
"title": "video 2"
}
....
]
}

- Return the list of all playlists:

{
"data" : [
{
"id": 1,
"name": "playlist 1"
....
},
{
"id": 2,
"name": "playlist 2"
}
….

]
}

- Create a playlist

- Show informations about the playlist

{
"data" : {
"id": 1,
"name": "playlist 1"
}
}

- Update informations about the playlist
- Delete the playlist
- Add a video in a playlist
- Delete a video from a playlist
- Return the list of all videos from a playlist (ordered by position):

{
"data" : [
{
"id": 1,
"title": "video 1 from playlist 2"
....
},
{
"id": 2,
"title": "video 2 from playlist 2"
}
....
]
}

Your goal: Design and build this API.

Important notes :
- Removing videos should re-arrange the order of your playlist and the storage.
- Python languages are supported
- Using frameworks is forbidden, your code should use native language libraries, except for Python, you could use bottlepy ( https://bottlepy.org/docs/dev/).
- Use Mysql for storing your data
- You should provide us the source code (or a link to GitHub) and the instructions to run your code