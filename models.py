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
   email = db.Column(db.String(200), unique=True, primary_key = True) 
   password = db.Column(db.String(100))
   education = db.Column(db.String(500))
   company = db.Column(db.String(500))
   job = db.Column(db.String(500))
   code = db.Column(db.String(100))
   java = db.Column(db.String(100))
   android = db.Column(db.String(100))
   answers = relationship("answers", uselist=False, back_populates="students")

   def __repr__(self):
        return '<User %r>' % (self.email)

# Final user answers
class answers(db.Model):
   __tablename__ = 'answers'
   id = Column(Integer, primary_key=True)
   students_email = Column(Integer, ForeignKey('students.email'))
   # when was user's last submission
   timestamp = db.Column(db.String(1000))
   answer_1 = db.Column(db.String(1000))
   answer_2 = db.Column(db.String(1000))
   answer_3 = db.Column(db.String(1000))
   answer_4 = db.Column(db.String(1000))
   answer_5 = db.Column(db.String(1000))
   answer_6 = db.Column(db.String(1000))
   answer_7 = db.Column(db.String(1000))
   students = relationship("students", back_populates="answers")

   def __repr__(self):
        return '<Answer %r>' % (self.students_email)

# History of what html pages (instructions, API, wiki) users opened
class timestamps(db.Model):
   __tablename__ = 'timestamps'
   id = Column(Integer, primary_key=True)
   email = db.Column(db.String(200))
   page = db.Column(db.String(1000))
   timestamp = db.Column(db.String(1000))

   def __repr__(self):
        return '<timestamps %r>'

# History of user's submissions and compile outputs
class submissions(db.Model):
   __tablename__ = 'submissions'
   id = Column(Integer, primary_key=True)
   email = db.Column(db.String(200))
   # no of the current submission
   count_submission = db.Column(Integer)
   # submission timestamp
   timestamp = db.Column(db.String(1000))
   # user answers
   answer = db.Column(db.String(5000))
   # compiler output
   output = db.Column(db.String(10000))

   def __repr__(self):
        return '<timestamps %r>'

'''
def __init__(self, name, surname, email, password):
   self.name = name
   self.surname = surname
   self.email = email.lower()
   self.password = password
'''