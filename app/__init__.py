from flask import Flask, session
from flask_session import Session
app = Flask(__name__)
# add_routes(app)
from app import views

# Flask-Session to store session data for each user on server
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

app.client_id = '8d433616e66144eb84618d4215334ebd'
app.client_secret = '818fc8631d3045fa87331b5bbd47ef6e'
app.redirect_uri = 'http://127.0.0.1:5000/login/callback'
