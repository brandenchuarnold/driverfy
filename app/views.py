# Base imports
from flask import render_template, session, url_for, redirect, request

# Library imports
import spotipy
import json, requests, time, random, string

# Custom imports
from app import app
from forms import *
import helpers


# / and /index are aliases of each other, but / takes priority
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/songs')
def songs():
    # If this is the first time, login and authorize
    if not 'authtoken' in list(session.keys()):
        return redirect(url_for('login'))

    # Renew access
    helpers.renewAccess()

    # Get content
    songs = requests.get('https://api.spotify.com/v1/me/tracks', headers={'Authorization': 'Bearer ' + session['accesstoken']}).json()
    print songs
    return render_template('songs.html', songs=songs['items'])


@app.route('/login')
def login():
    scope = 'playlist-modify-private user-library-read'
    return redirect('https://accounts.spotify.com/authorize/?client_id=' + app.client_id + '&response_type=code&scope=' + scope + '&redirect_uri=' + app.redirect_uri)


@app.route('/login/callback')
def login_callback():
    session['authtoken'] = request.args.get('code')
    return redirect(url_for('songs'))


@app.route('/session/start')
def start_session():
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))

    session['drivekey'] = key
    app.sessions[key] = {'accesstoken': session['accesstoken'],
                            'expiration': session['expiration'],
                            'refreshtoken': session['refreshtoken']}

    return render_template('driver_interface.html', key=session['drivekey'])

@app.route('/session/join')
def join_session():
    form = SessionForm(request.form)
    if request.method == 'POST' and form.validate():
        session_key = form.session_id.data
        if session_key and not session_key in app.sessions.keys():
            return redirect('/session/join', message='No drive with that ID exists!')
        elif session_key:
            session['drivekey'] = session_key
            tokens = app.sessions[session['drivekey']]
            session['refreshtoken'] = tokens['refreshtoken']
            helpers.renewAccess()

        return render_template('songs.html', form=form)

    return render_template('join_session.html', form=form)
