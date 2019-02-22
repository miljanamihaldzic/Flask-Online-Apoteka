from wtforms import Form, StringField, TextAreaField, PasswordField,validators,SubmitField
from passlib.hash import sha256_crypt
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm

class CategoryForm(Form):
    name = StringField('Name', [validators.Length(min =1, max = 50)])
    description = TextAreaField('Desctiption', [validators.Length(min =6, max = 550)])
    picture = FileField('Add picture for category', validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Save')
    