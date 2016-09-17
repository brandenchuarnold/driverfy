from flask import Blueprint, jsonify, request
import httplib

from session import join_session, leave_session

session_route = Blueprint('session', __name__)

@session_route.route('/join/', methods=['PUT'])
def join_session_get_result():
    session_json = request.json

    if session_json:
        status = httplib.OK
        session_status = join_session(session_json['session_id'])

        return jsonify(session_status=session_status)

    return "Invalid Parameter", httplib.BAD_REQUEST

@session_route.route('/leave/', methods=['PUT'])
def leave_session_get_result():
    session_json = request.json

    if session_json:
        status = httplib.OK
        session_status = leave_session(session_json['session_id'])

        return jsonify(session_status=session_status)

    return "Invalid Parameter", httplib.BAD_REQUEST
