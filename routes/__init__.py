from flask import (
    Blueprint,
    current_app as app,
    jsonify
)
from routes.playlist import (
    playlist_route
)

def add_routes(app):
    app.register_blueprint(playlist_route, url_prefix="/playlist")
