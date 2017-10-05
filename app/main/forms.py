from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    from_locale = StringField('From Locale', validators=[Required()])
    to_locale = StringField('To Locale', validators=[Required()])
    submit = SubmitField('Enter Chatroom')
