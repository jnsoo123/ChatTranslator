#!/bin/env python
from app import create_app, socketio, database
from flask import g

app = create_app(debug=True)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.cli.command('initdb')
def initdb_command():
    database.init_db()
    print('Database Initialized')

if __name__ == '__main__':
    socketio.run(app)
