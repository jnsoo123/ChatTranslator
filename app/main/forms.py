from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    from_locale = SelectField('From Locale', choices=[('en-US', 'US English'), ('ja', 'Japanese'), ('zh-TK', 'Chinese')], validators=[Required()])
    to_locale = SelectField('To Locale', choices=[('en-US', 'US English'), ('ja', 'Japanese'), ('zh-TK', 'Chinese')], validators=[Required()])
    submit = SubmitField('Join Room')
