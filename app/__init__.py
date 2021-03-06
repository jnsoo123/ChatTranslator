from flask import Flask
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import os

socketio = SocketIO()

def create_app(debug=True):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'chat.db'),
        SECRET_KEY='gjr39dkjn344_!67#',
        USERNAME='admin',
        PASSWORD='default',
        PREFERRED_URL_SCHEME='https'
    ))

    Bootstrap(app)

    import eventlet

    eventlet.sleep()
    eventlet.monkey_patch()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

