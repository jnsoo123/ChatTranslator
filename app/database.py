import sqlite3
import chat
from flask import g

def get_app():
    return chat.app

def connect_db():
    """Connects to the database."""
    app = get_app()
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    print('Database Connected')
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    app = get_app()
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
