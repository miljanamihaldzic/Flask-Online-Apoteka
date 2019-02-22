from wtforms import Form, StringField, TextAreaField, PasswordField,validators,SubmitField,SelectField,IntegerField
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm

class ProductForm(FlaskForm):
    name = StringField('Name', [validators.Length(min =1, max = 50)])
    description = TextAreaField('Description', [validators.Length(min =6, max = 550)])
    price = IntegerField('Price',[validators.NumberRange(min =1)])
    category = SelectField('Category',choices=[])
    picture = FileField('Add picture for product', validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Save')
    