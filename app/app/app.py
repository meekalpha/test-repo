import os
import sqlite3
import datetime

from .ecusis import EcusisSource

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from .database import db_session, prep_db
from .models import TimeSlot

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True)

def init_ecusis(username, password):
    session['ecusis_source'] = EcusisSource(username, password)

def get_ecusis():
    if not hasattr(g, 'ecusis_source'):
        g.ecusis_source = EcusisSource(session['username'], session['password'])
    return g.ecusis_source

def add_or_update(timeslot):
    existing = db_session.query(TimeSlot)\
        .filter_by(room_id=timeslot.room_id)\
        .filter_by(start_time=timeslot.start_time)\
        .first()
    if existing:
        existing.update_from(timeslot)
        db_session.merge(existing)
    if not existing:
        db_session.add(timeslot)
    db_session.commit()

def remote_update_db(room_id):
    ecusis = get_ecusis()
    timeslots = ecusis.get_time_slots(room_id)
    for t in timeslots:
        add_or_update(t)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/', methods=['GET', 'POST'])
def show_timeslots():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    room_id = None
    if request.method == 'POST':
        room_id = request.form['roomId']

    if (room_id):
        remote_update_db(room_id)

    timeslots = TimeSlot.query.filter_by(room_id = room_id)
    rooms = ["200011123", "200011125", "200011130", "200011131", "200011133", "200011142", "200012210", "200012234"]
    return render_template('show_timeslots.html', rooms=rooms, timeslots=timeslots)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #TODO: obviously this is bad. We need to login, which confirms these credentials,
        # then hang on to the login cookie we get in return.. or something.
        # http requests are stateless so we can't maintain EcusisSource between requests.
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('show_timeslots'))
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('password', None)
    flash('You were logged out')
    return redirect(url_for('login'))
