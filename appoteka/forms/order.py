from wtforms import Form, StringField, TextAreaField, PasswordField,validators,SubmitField,SelectField,IntegerField
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm

class OrderForm(FlaskForm):
    first_name = StringField('First name', [validators.Length(min =1, max = 50)])
    last_name = StringField('Last name', [validators.Length(min =1, max = 50)])
    
    username = StringField('Username', [validators.Length(min =1, max = 50)])
    email = StringField('Email', [validators.Length(min =1, max = 50)])
    address = StringField('Address', [validators.Length(min =1, max = 50)])
    country = StringField('Country', [validators.Length(min =1, max = 50)])
    zip_code = StringField('Zip code', [validators.Length(min =1, max = 50)])
    
    payment_method = SelectField('Payment',choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('PayPal','PayPal')])
    
    name_on_card = StringField('Name on card', [validators.Length(min =1, max = 50)])
    credit_card_number = StringField('Credit card number', [validators.Length(min =1, max = 50)])
    expiration = StringField('Expiration', [validators.Length(min =1, max = 50)])
    cvv = StringField('CVV', [validators.Length(min =1, max = 50)])
    
    submit = SubmitField('Continue to checkout')
    