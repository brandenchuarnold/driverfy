from wtforms import Form, IntegerField, BooleanField, validators

class LoginForm(Form):
    session_id = IntegerField('Session ID:', [validators.DataRequired()])
    create_mode = BooleanField('Check to make new Session:', [validators.DataRequired()])
