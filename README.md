Simple Chat Auto Translator
===================

**How To Run**
- run `pip install -r requirements.txt`
- run `export FLASK_APP=chat.py`
- run `flask initdb`
When in development:
- run `gunicorn --certfile cert.pem --keyfile key.pem -b 127.0.0.1:5000 chat:app --log-level debug --workers=1 --worker-class eventlet --timeout 36`
When in production:
- run `gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:5000 chat:app --log-level debug --workers=1 --worker-class eventlet --timeout 36`
