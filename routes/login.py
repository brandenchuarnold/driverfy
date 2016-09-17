from flask import Blueprint, jsonify, request
import httplib

from login import login_user, logout_user

login_route = Blueprint('login', __name__)

@login_route.route('/login/', methods=['PUT'])
def login_user_get_result():
    login_json = request.json

    if login_json:
        status = httplib.OK
        login_status = login_user(login_json['user_id'])

        return jsonify(login_status=login_status)

    return "Invalid Parameter", httplib.BAD_REQUEST

@login_route.route('/logout/', methods=['PUT'])
def logout_user_get_result():
    login_json = request.json

    if login_json:
        status = httplib.OK
        login_status = logout_user(login_json['user_id'])

        return jsonify(login_status=login_status)

    return "Invalid Parameter", httplib.BAD_REQUEST


