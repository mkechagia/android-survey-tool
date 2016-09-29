from flask import Flask
from flask_wtf import Form
from wtforms import TextField, BooleanField, StringField, TextAreaField, SubmitField, PasswordField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from models import db, students

class SignupForm(Form):
    email = EmailField('email', [validators.Email("Please enter your email address.")])
    password = PasswordField('password')
    education = TextField('education')
    company = TextField('company')
    job = TextField('job')
    code = TextField('code')
    java = TextField('java')
    android = TextField('android')
    submit = SubmitField('submit')