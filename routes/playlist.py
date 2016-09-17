from flask import Blueprint, jsonify
import httplib

from playlist import (
    get_playlist_by_session_id as get_playlist,
    move_track
)

playlist_route = Blueprint('playlist', __name__)


@playlist_route.route('/get_playlist/<int:session_id>', methods=['GET'])
def get_playlist_by_session_id(session_id):
    if session_id > 0:
        playlist_data = get_playlist_by_session_id(session_id)
        if playlist_data:
            status = httplib.OK
        else:
            status = httplib.NOT_FOUND
        return jsonify(playlist=playlist_data), status

    return "Invalid Parameter", httplib.BAD_REQUEST

@playlist_route.route('/move_track/', methods=['POST'])
def move_track_location()
    track_json = request.json
    if track_json is not None:
        status = httplib.OK
        move_status = move_track(track_json['track_id'],
                                 track_json['index_from'],
                                 track_json['index_to'])
        return jsonify(move_status=move_status), status
    return "Invalid Parameter", httplib.BAD_REQUEST
