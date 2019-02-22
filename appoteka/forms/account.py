from wtforms import Form, StringField, TextAreaField, PasswordField,validators,SubmitField
from flask_wtf import FlaskForm
from flask_login import current_user
from appoteka.models.user import User
from flask_wtf.file import FileField, FileAllowed

class AccountForm(FlaskForm):
    username = StringField('Username', [validators.Length(min =1, max = 50)])
    email = StringField('Email', [validators.Length(min =6, max = 50)])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')


    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one.')
        
    