from wtforms import Form, StringField, validators

class SessionForm(Form):
    session_id = StringField('Session ID:', [validators.DataRequired()])
