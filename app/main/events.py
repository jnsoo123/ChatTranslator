from flask import session
from flask_socketio import emit, join_room, leave_room
from translate import Translator
from .. import socketio
from .. import database
import urllib

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""

    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""

    print message

    text                = message['msg']
    room                = session.get('room')
    name                = session.get('name')
    translation_locale  = session.get('to_locale')
    original_locale     = session.get('from_locale')

    translator      = Translator(to_lang=translation_locale, from_lang=original_locale)
    translated_text = translate_text(text, translator)

    message = u"{0}: {1} ({2}: {3})".format(name, translated_text, original_locale, text)

    db = database.get_db()
    db.execute('insert into messages (user, message, room) values (?, ?, ?)', [name, message, room])
    db.commit()

    emit('message', {'msg': message}, room=room) 

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""

    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

@socketio.on('change_locale', namespace='/chat')
def change_locale(data):
    """Change locale of the current user"""

    session[data['type']] = data['locale']

def translate_text(text, translator):
    """Translate the text.""" 

    try:
        translated_text = translator.translate(text)
    except KeyError:
        try:
            translated_text = translator.translate(str(text))
        except UnicodeEncodeError:
            translated_text = urllib.quote(translator.translate(text.encode('utf-8')))
        except UnicodeEncodeError:
            translated_text = urllib.quote(translator.translate(text.encode('utf-8')))

    return urllib.unquote(translated_text)
