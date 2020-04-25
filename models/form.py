from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField, TextAreaField, StringField
from wtforms.validators import Length, Email, Required

class ContactForm(FlaskForm):
    contents = TextAreaField("Please leave message or question (2048 characters)", validators=[Required(),Length(max=2047)])
    email = StringField("Enter Your Email Address", validators=[Required(), Email()])
    recaptcha = RecaptchaField()
    
    