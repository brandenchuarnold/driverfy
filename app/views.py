from flask import render_template, session, url_for, redirect, request, current_app
from app import app
from forms import SessionForm

from logic.playlist import make_playlist

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/songs')
def songs():
    if not 'user' in list(session.keys()):
        return redirect(url_for('login'))
    return render_template('songs.html')

@app.route('/session')
def session():
    form = SessionForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.driver_id:
            app.sessions[len(sessions)] = form.driver_id.data
            make_playlist(session_id)
            return redirect(url_for('songs.html'), session_id=(len(sessions) - 1))
        elif form.session_id:
            return redirect(url_for('songs.html'), session_id=session_id)
    return render_template('session.html', form=form)
