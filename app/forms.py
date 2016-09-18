from wtforms import Form, StringField, validators

# Drive session form to take in a single ID, the drive session ID (as shown to driver)
class SessionForm(Form):
    session_id = StringField('Session ID:', [validators.DataRequired()])
