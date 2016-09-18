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
    # Display index.html (consisting of logo and session start/join)
    return render_template('index.html')


@app.route('/songs')
def songs():
    # If this is the first time, login and authorize
    if not 'authtoken' in session.keys() and not 'refreshtoken' in session.keys():
        return redirect(url_for('login'))

    # Renew access
    helpers.renewAccess()

    # Get relevant playlist


    # return str(playlistdata)
    songs = requests.get('https://api.spotify.com/v1/me/tracks', headers={'Authorization': 'Bearer ' + session['accesstoken']}).json()


    return render_template('songs.html', songs=songs['items'], key=session['drivekey'])


@app.route('/login')
def login():
    # If we have a refresh token, go ahead and just go straight to songs since the songs route will automatically renew access
    if 'refreshtoken' in session.keys():
        return redirect(url_for('songs'))

    # Set scope parameter
    scope = 'playlist-read-private playlist-modify-private user-library-read'

    # Redirect to the spotify login site
    return redirect('https://accounts.spotify.com/authorize/?client_id=' + app.client_id + '&response_type=code&scope=' + scope + '&redirect_uri=' + app.redirect_uri)


@app.route('/login/callback')
def login_callback():
    # Store the authorization token retrieved from Spotify, and obtain/store access and renewal tokens
    session['authtoken'] = request.args.get('code')
    helpers.renewAccess()

    # Send the user back home
    return redirect('/')


@app.route('/session/start')
def start_session():

    # If we don't have any authtokens in our session, we need to log in
    if not 'authtoken' in session.keys() or not session['authtoken']:
        return redirect(url_for('login'))

    # Make double sure we have all our tokens
    helpers.renewAccess()

    # If we get here, we're authorized. Generate a random session key (this is of order 36^6 so I don't anticipate collisions especially with random.SystemRandom(), but if this gets big in the future we should change this)
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))

    # Store the key in the session, and store our tokens in the global sessions obj
    session['drivekey'] = key
    app.sessions[key] = {'accesstoken': session['accesstoken'],
                            'expiration': session['expiration'],
                            'refreshtoken': session['refreshtoken']}

    # Retrieve playlist data about the current user and extract names
    playlistdata = requests.get('https://api.spotify.com/v1/me/playlists', headers={'Authorization': 'Bearer ' + session['accesstoken']}).json()

    playlists = map(lambda item: item['name'], playlistdata['items'])

    # If there doesn't exist a "Driverfy Playlist" playlist, make one and store the returned ID
    userdata = requests.get('https://api.spotify.com/v1/me/', headers={'Authorization': 'Bearer ' + session['accesstoken']}).json()
    if not 'Driverfy Playlist' in playlists:
        headers = {'Authorization': 'Bearer {0}'.format(session['accesstoken']), 'Content-Type': 'application/json'}
        body = {'name': 'Driverfy Playlist', 'public': 'false'}
        session['plid'] = requests.post('https://api.spotify.com/v1/users/{0}/playlists'.format(userdata['id']), headers=headers, data=body)
        app.sessions[key]['plid'] = session['plid']

    # Otherwise, go back through playlist data, find the relevant ID and store it + clear the playlist
    else:
        session['plid'] = playlistdata['items'].filter(lambda x: x['name'] == 'Driverfy Playlist')[0]['id']
        app.sessions[key]['plid'] = session['plid']
        headers = {'Authorization': 'Bearer {0}'.format(session['accesstoken'])}
        trackIDs = map(lambda x: {'uri': x['track']['uri']}, requests.get('http://api.spotify.com/v1/users/{0}/playlists/{1}'.format(userdata['id'], session['plid']), headers=headers)['items'])
        headers['Content-Type'] = 'application/json'
        requests.delete('https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks', headers=headers, body={'tracks': trackIDs})

    # Mark this session as the session starter
    app.sessions[key]['origin'] = True

    # Done setting up! Redirect now to our queue page
    return redirect(url_for('songs'))

@app.route('/session/join', methods=['GET', 'POST'])
def join_session():

    # Create form for taking in the drive session ID
    form = SessionForm(request.form)

    # If posted valid result...
    if request.method == 'POST' and form.validate():

        # Extract key and check if extant, redirecting to join again if not
        session_key = form.session_id.data
        if session_key and not session_key in app.sessions.keys():
            return redirect('/session/join')

        # Store the drive key, get the relevant tokens from the sessions global, and force renewal of tokens to ensure current session is up to date
        session['drivekey'] = session_key
        tokens = app.sessions[session['drivekey']]
        session['refreshtoken'] = tokens['refreshtoken']
        helpers.renewAccess(force=True)

        # Redirect to songs page
        return redirect(url_for('songs'))

    # By default, render the "join a drive session" page
    return render_template('join_session.html', form=form)
