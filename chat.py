#!/bin/env python
from app import create_app, socketio, database
from flask import g, jsonify, request, session
import subprocess as sp
import speech_recognition as sr
import os
from pydub import AudioSegment

app = create_app(debug=False)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.cli.command('initdb')
def initdb_command():
    database.init_db()
    print('Database Initialized')

@app.route('/_record_voice', methods=['POST'])
def record_voice():
    remove_files()
    try:
        lang = request.form.get('language')

        f = open('speech.ogg', 'wb')
        f.write(request.files['file'].read())
        f.close()

        sound = AudioSegment.from_file('speech.ogg')
        sound.export('speech.wav', format='wav')

        r = sr.Recognizer()
        with sr.AudioFile('speech.wav') as source:
            audio = r.record(source)
        
        text = r.recognize_google(audio, language=str(lang))
    except Exception as e:
        print e
        text = 'Unable to understand'
    finally:
        return jsonify(text)

def remove_files():
    array_files = ['speech.ogg', 'speech.wav']
    for f in array_files:
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':
    socketio.run(app)
