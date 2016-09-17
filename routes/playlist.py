from flask import Blueprint, jsonify
import httplib

from playlist import (
    get_playlist,
    add_track,
    move_track,
    remove_track
)

playlist_route = Blueprint('playlist', __name__)


@playlist_route.route('/get_playlist/<int:session_id>', methods=['GET'])
def _get_playlist(session_id):
    if session_id > 0:
        playlist_data = get_playlist(session_id)
        if playlist_data:
            status = httplib.OK
        else:
            status = httplib.NOT_FOUND
        return jsonify(playlist=playlist_data), status

    return "Invalid Parameter", httplib.BAD_REQUEST


@playlist_route.route('/add_track/', methods=['POST'])
def _add_track():
    track_json = request.json
    if track_json is not None:
        add_status = add_track(track_json['session_id'],
                               track_json['index_from'],
                               track_json['index_to'])
        return httplib.OK
    return httplib.BAD_REQUEST


@playlist_route.route('/move_track/', methods=['POST'])
def _move_track():
    track_json = request.json
    if track_json is not None:
        status = httplib.OK
        move_status = move_track(track_json['session_id'],
                                 track_json['index_from'],
                                 track_json['index_to'])
        return httplib.OK
    return httplib.BAD_REQUEST


@playlist_route.route('/move_track/', methods=['POST'])
def _remove_track():
    track_json = request.json
    if track_json is not None:
        status = httplib.OK
        remove_status = remove_track(track_json['session_id'],
                                     track_json['index_from'],
                                     track_json['index_to'])
        return httplib.OK
    return httplib.BAD_REQUEST
