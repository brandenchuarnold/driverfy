from flask import Flask, session
from flask_session import Session
from routes import add_routes

app = Flask(__name__)
add_routes(app)
from app import views

# Flask-Session to store session data for each user on server
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

print app

app.client_id = '30d99d3880fd49e0a9030797b7d1ed5b'
app.client_secret = '95d94dbeab424290938bdbce098f52e9'
app.redirect_uri = 'driverfy.herokuapp.com'

print app
