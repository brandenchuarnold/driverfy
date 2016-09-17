import spotipy
from flask import current_app as app


def search_song(session_id,
                song_text):
    return app.sp.search(q=song_text,
                         limit=SONG_LIMIT,
                         offset=0,
                         type='track')
