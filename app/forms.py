from wtforms import Form, StringField, validators

class SessionForm(Form):
    session_id = StringField('Session ID:', [validators.Length(min=6, max=6, message="Must be length 6!")])
