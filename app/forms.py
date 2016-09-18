from wtforms import Form, StringField, PasswordField, BooleanField, validators

class LoginForm(Form):
    email = StringField('Spotify email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
