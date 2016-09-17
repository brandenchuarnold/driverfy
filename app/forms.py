from wtforms import Form, IntegerField

class SessionForm(Form):
    driver_id = IntegerField('Create Session', [])
    session_id = IntegerField('Join a Session', [])
