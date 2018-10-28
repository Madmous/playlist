"""This module does blah blah."""
import os
import MySQLdb

from bottle_mysql import Plugin
from bottle import default_app

from playlist import playlist_api
from video import video_api
from database import create_schema_if_necessary

app = default_app()
db_name = os.environ["DB"]
plugin = Plugin(dbuser=os.environ["USER"],
                dbpass=os.environ["PASSWORD"], dbname=db_name)
app.install(plugin)

if __name__ == '__main__':
    create_schema_if_necessary(db_name)
    app.run(host='127.0.0.1', port=8080)
