from flask import session

import requests, time

from app import app


def renewAccess(force=False):
    if not force and 'expiration' in session.keys() and session['expiration'] > time.time():
        return
    if 'refreshtoken' in session.keys():
        postbody = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refreshtoken'],
            'client_id': app.client_id,
            'client_secret': app.client_secret
        }
    else:
        postbody = {
            'grant_type': 'authorization_code',
            'code': session['authtoken'],
            'redirect_uri': app.redirect_uri,
            'client_id': app.client_id,
            'client_secret': app.client_secret
        }
    try:
        tokens = requests.post(url='https://accounts.spotify.com/api/token', data=postbody).json()

        print tokens

        session['accesstoken'] = tokens['access_token']
        session['expiration'] = time.time() + tokens['expires_in']
        if 'refresh_token' in tokens.keys():
            session['refreshtoken'] = tokens['refresh_token']
        return True
    except ValueError:
        return False
