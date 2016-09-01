from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from signup import SignupForm
from models import app, db, students, answers
import validators
from validators import email
import os
from sqlalchemy import update
#from flask_login import login_user , logout_user , current_user , login_required
import json
from collections import defaultdict
from subprocess import check_output
from glue import glue_answer

global dict
dict = {}

@app.route('/')
def index():
   return render_template('index.html')

# add new user
@app.route('/new', methods = ['GET', 'POST'])
def new():
	if (request.method == 'POST'):
		if (not request.form['name'] or not request.form['surname'] or not request.form['email'] or not request.form['password']):
			flash('Please enter all the fields.', 'error')
		else:
			student = students(name=request.form['name'], surname=request.form['surname'], email=request.form['email'], password=request.form['password'])
			# check if the email already exists---unique user
			if (not db.session.query(students.id).filter(students.email==student.email).count() == 0):
				flash('The email is already taken.', 'error')
			else:
				# check for valid email address
				is_valid = email(student.email)
				if (is_valid):
					# create a new student
					db.session.add(student)
					db.session.commit()
					session['email'] = student.email
					flash('Record was successfully added.')
					return redirect(url_for('show_all'))
					#return render_template('form_submit.html', student=student)
				else:
					flash('The email is not valid.', 'error')
	return render_template('new.html')

# Define a route for the action of the form, for example '/survey/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/survey/', methods=['POST'])
def survey():
    if ('email' in session):
    	dict = {}
    	answer=answers.query.filter_by(students_email=session['email']).first()
    	# update user's answers when login, edit answer boxes, and submit
    	if (not db.session.query(answers.id).filter(answers.students_email==session['email']).count() == 0):
    		#update(answers).where(answers.students_email==session['email']).values(answer_1=request.form['hiddeninput_delete'])
    		answer.answer_1=request.form['hiddeninput_delete']
    		#db.session.add(answer)
    		db.session.commit()
    	else:
    		# add user answers to the db
    		answer = answers(students_email=session['email'], answer_1=request.form['hiddeninput_delete'])
    		db.session.add(answer)
    		db.session.commit()
    	# add user answers to .json file
    	dict["answer_1"] = request.form['hiddeninput_delete']
    	file_name = session['email']+'.json'
    	with open(file_name, 'w') as fp:
    		json.dump(dict, fp, indent = 4)
    return render_template('form_action.html', answer=answer)

# show all users
@app.route('/show_all')
def show_all():
   return render_template('show_all.html', students = students.query.all())

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	student = students.query.filter_by(email=email, password=password).first()
	if student is None:
		flash('Username or Password is invalid' , 'error')
		return render_template('index.html', student=student)
	else:
		session['logged_in'] = True
		session['email'] = email
		answ=answers.query.filter_by(students_email=session['email']).first()
		return render_template('form_submit.html', answ=answ)

# compiler results
@app.route('/results.html')
def results():
	if ('email' in session):
                answer=answers.query.filter_by(students_email=session['email']).first()
                answ = answer.answer_1
                java_file_complete = glue_answer(answ)
                # XXX: environment-specific path to Android project
                project_path = "NotePad/src/com/example/android/notepad"
                with open("%s/NoteEditor.java" % project_path, "w") as f:
                    f.write("%s" % java_file_complete)
                javac_output = check_output(["cd", "NotePad", "&&", "ant", "debug"])
		return render_template('results.html', answ=javac_output)

@app.route('/logout.html')
def logout():
	if 'email' not in session:
		return redirect(url_for('index'))

	session.pop('email', None)
	return render_template('logout.html')

if __name__ == '__main__':
   db.create_all()
   app.run(host='0.0.0.0', debug = True)
