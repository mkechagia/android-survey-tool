from flask import Flask
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from models import db, students

class SignupForm(Form):
    name = TextField('name')
    surname = TextField('surname')
    email = EmailField('email', [validators.Email("Please enter your email address.")])
    password = PasswordField('password')
    submit = SubmitField('submit')