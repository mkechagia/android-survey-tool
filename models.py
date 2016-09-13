from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
   __tablename__ = 'students'
   id = db.Column('student_id', db.Integer, unique=True)
   email = db.Column(db.String(200), unique=True, primary_key = True) 
   password = db.Column(db.String(100))
   job = db.Column(db.String(1000))
   code = db.Column(db.String(100))
   android = db.Column(db.String(100))
   answers = relationship("answers", uselist=False, back_populates="students")

   def __repr__(self):
        return '<User %r>' % (self.email)

class answers(db.Model):
   __tablename__ = 'answers'
   id = Column(Integer, primary_key=True)
   students_email = Column(Integer, ForeignKey('students.email'))
   answer_1 = db.Column(db.String(1000))
   answer_2 = db.Column(db.String(1000))
   answer_3 = db.Column(db.String(1000))
   answer_4 = db.Column(db.String(1000))
   answer_5 = db.Column(db.String(1000))
   answer_6 = db.Column(db.String(1000))
   answer_7 = db.Column(db.String(1000))
   answer_8 = db.Column(db.String(1000))
   answer_9 = db.Column(db.String(1000))
   answer_10 = db.Column(db.String(1000))
   students = relationship("students", back_populates="answers")

   def __repr__(self):
        return '<Answer %r>' % (self.students_email)


'''
def __init__(self, name, surname, email, password):
   self.name = name
   self.surname = surname
   self.email = email.lower()
   self.password = password
'''