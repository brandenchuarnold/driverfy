from spotipy import Spotify, util
from flask import current_app as app

DRIVER_PLAYLIST_NAME = 'driverfy'

def make_playlist(session_id):
    user_id = app.sessions[session_id]
    app.sp.user_playlist_create(user=user_id,
                                name=DRIVER_PLAYLIST_NAME,
                                public=False)
    return 'Success'


def get_playlist(session_id):
    if session_id not in app.sessions:
        return None
    user_id = app.sessions[session_id]
    playlists = sp.user_playlists(user=user_id)
    playlist = playlists[DRIVER_PLAYLIST_NAME]
    return playlist


def add_track(session_id,
              track_id):
    playlist = get_playlist_by_session(session_id)
    if playlist is None:
        return None
    app.sp.user_playlist_add_tracks(user=app.sessions[sesison_id],
                                    playlist_id=playlist['id'],
                                    tracks=[track_id],
                                    position=None)
    return 'Success'


def move_track(session_id,
               track_index_from,
               track_index_to):
    playlist = get_playlist_by_session(session_id)
    if playlist is None:
        return None
    app.sp.user_playlist_reorder_tracks(user=app.sessions[session_id],
                                        playlist_id=playlist['id'],
                                        range_start=track_index_from,
                                        range_length=1,
                                        insert_before=track_index_to,
                                        snapshot_id=None)
    return 'Success'

def remove_track(session_id,
                 track_index):
    playlist = get_playlist_by_session(session_id)
    if playlist is None:
        return None
    app.sp.user_playlist_remove_specific_occurnences_of_tracks(user=app.sessions[session_id],
                                                               playlist_id=playlist['id'],
                                                               tracks=[{'uri': playlist['tracks'][track_index_from]['id'],
                                                                        'positions': [track_index_from]}],
                                                               snapshot_id=None)
    return 'Success'

