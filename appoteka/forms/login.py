from wtforms import Form, StringField, TextAreaField, PasswordField,validators,BooleanField
from passlib.hash import sha256_crypt

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
    remember = BooleanField('Remember Me')
    
    