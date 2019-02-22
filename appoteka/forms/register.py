from wtforms import Form, StringField, TextAreaField, PasswordField,validators
from passlib.hash import sha256_crypt

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min =1, max = 50)])
    email = StringField('Email', [validators.Length(min =6, max = 50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')
    