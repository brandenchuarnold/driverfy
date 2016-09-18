from wtforms import Form, IntegerField, BooleanField, validators

class SessionForm(Form):
    session_id = IntegerField('Session ID:', [validators.DataRequired()])
