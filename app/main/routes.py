from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from flask_bootstrap import Bootstrap
from .. import database

@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()

    if form.validate_on_submit():
        session['name']         = form.name.data
        session['room']         = form.room.data
        session['from_locale']  = form.from_locale.data
        session['to_locale']    = form.to_locale.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data          = session.get('name', '')
        form.room.data          = session.get('room', '')
        form.from_locale.data   = session.get('from_locale', '')
        form.to_locale.data     = session.get('to_locale', '')

    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')

    db       = database.get_db()
    cur      = db.execute('select message from messages where room = ? order by id desc', [room])
    messages = cur.fetchall()

    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, messages=messages)
