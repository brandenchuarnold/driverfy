from flask import render_template, session, url_for, redirect, request
from app import app
from forms import *
import spotipy

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/songs')
def songs():
    if not 'user' in list(session.keys()):
        return redirect(url_for('login'))
    return render_template('songs.html')

@app.route('/login')
def login():
    form = LoginForm(request.form)
    # if request.method == 'POST' and form.validate():
    return render_template('login.html', form=form)
