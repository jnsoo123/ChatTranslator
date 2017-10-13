from __future__ import unicode_literals
from flask import session, redirect, url_for, render_template, request, jsonify
from . import main
from .forms import LoginForm
from flask_bootstrap import Bootstrap
from .. import database
import youtube_dl
import os
import speech_recognition as sr
from pydub import AudioSegment

@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()

    if form.validate_on_submit():
        session['name']         = form.name.data
        session['room']         = form.room.data
        session['from_locale']  = form.from_locale.data
        session['to_locale']    = form.to_locale.data
        return redirect(url_for('.chat', _scheme='https', _external=True))
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
    cur      = db.execute('select message from messages where room = ? order by id asc', [room])
    messages = cur.fetchall()

    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, messages=messages)

@main.route('/transcript')
def transcript():
    """YT Transcript Page."""
    return render_template('transcript.html')

@main.route('/_transcribe', methods=['POST'])
def transcribe():
    """Transcribes youtube video to text."""

    array_files = ['transcript.mp3', 'text.wav']
    for f in array_files:
        if os.path.exists(f):
            os.remove(f)

    try:
        url = request.form.get('url')
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'outtmpl': 'transcript.%(ext)s'
        }
    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        sound = AudioSegment.from_file('transcript.mp3')
        sound.export('text.wav', format='wav')

        r = sr.Recognizer()
        with sr.AudioFile('text.wav') as source:
            audio = r.record(source)

        text = r.recognize_sphinx(audio)
        return jsonify(text)
    except Exception:
        return jsonify('error')
