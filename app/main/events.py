from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from translate import Translator

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
    text = message['msg']
    room = session.get('room')
    translate = Translator(to_lang=session.get('to_locale'), from_lang=session.get('from_locale'))

    try:
        translated_text = translate.translate(text)
    except KeyError:
        try:
            translated_text = translate.translate(str(text))
        except UnicodeEncodeError:
            translated_text = urllib.quote(translate.translate(text.encode('utf-8')))
        except UnicodeEncodeError:
            translated_text = urllib.quote(translate.translate(text.encode('utf-8')))

    emit('message', {'msg': session.get('name') + ':' + translated_text}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

@socketio.on('change_locale', namespace='/chat')
def change_locale(locale):
    """Change locale of the current user"""
    session['to_locale'] = locale['locale']
