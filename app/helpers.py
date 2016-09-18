def renewAccess():
    if 'refreshtoken' in list(session.keys()):
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
        session['accesstoken'] = tokens['access_token']
        session['expiration'] = time.time() + tokens['expires_in']
        session['refreshtoken'] = tokens['refresh_token']
        return True
    except ValueError:
        return False
