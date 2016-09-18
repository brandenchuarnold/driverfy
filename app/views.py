from flask import render_template, session, url_for, redirect, request
from app import app
from forms import *
import spotipy
import json, requests, time

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/songs')
def songs():
    # If this is our first time, login and authorize
    if not 'authtoken' in list(session.keys()):
        return redirect(url_for('login'))
    # If we've passed the expiration of the previous access token retrieval
    elif 'expiration' in list(session.keys()) and time.time() > session['expiration']:
        postbody = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refreshtoken'],
            'client_id': app.client_id,
            'client_secret': app.client_secret
        }
    # If we've retrieved an authorization token for the first time, and therefore not yet processed tokens
    elif 'authtoken' in list(session.keys()) and not 'expiration' in list(session.keys()):
        postbody = {
            'grant_type': 'authorization_code',
            'code': session['authtoken'],
            'redirect_uri': app.redirect_uri,
            'client_id': app.client_id,
            'client_secret': app.client_secret
        }
        tokens = requests.post(url='https://accounts.spotify.com/api/token', data=postbody).json()
        print tokens
        session['accesstoken'] = tokens['access_token']
        session['expiration'] = time.time() + tokens['expires_in']
        session['refreshtoken'] = tokens['refresh_token']

    # Get content
    songs = requests.get('https://api.spotify.com/v1/me/tracks', headers={'Authorization': 'Bearer ' + session['accesstoken']}).json()['items']
    return render_template('songs.html', songs=songs)

@app.route('/login')
def login():
    scope = 'playlist-modify-private user-library-read'
    return redirect('https://accounts.spotify.com/authorize/?client_id=' + app.client_id + '&response_type=code&scope=' + scope + '&redirect_uri=' + app.redirect_uri)

@app.route('/login/callback')
def login_callback():
    session['authtoken'] = request.args.get('code')
    return redirect(url_for('songs'))
