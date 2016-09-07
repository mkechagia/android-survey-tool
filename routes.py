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
from subprocess import Popen, PIPE, TimeoutExpired
from glue import glue_answer, replace_methods
import format_answer

global dict
dict = {}
global answ
answ = {}

# Glue user's answers to the NoteEditor.java
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/new', methods = ['GET', 'POST'])
def new():
	if (request.method == 'POST'):
		if (not request.form['name'] or not request.form['surname'] or not request.form['email'] or not request.form['password'] or not request.form['secret']):
			flash('Please enter all the fields.', 'error')
		else:
			student = students(name=request.form['name'], surname=request.form['surname'], email=request.form['email'], password=request.form['password'], secret=request.form['secret'])
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
					#return redirect(url_for('show_all')) -> this is for debugging
					session['logged_in'] = True
					answ=answers.query.filter_by(students_email=session['email']).first()
					return render_template('form_submit.html', answ=answ)
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
    	answ=answers.query.filter_by(students_email=session['email']).first()
    	# update user's answers when login, edit answer boxes, and submit
    	if (not db.session.query(answers.id).filter(answers.students_email==session['email']).count() == 0):
    		# format user's answer
    		first_answer=format_answer.format_answer(request.form['hiddeninput_delete'])
    		answ.answer_1=first_answer
    		db.session.commit()
    	else:
    		# format user's answer
    		first_answer=format_answer.format_answer(request.form['hiddeninput_delete'])
    		# add user answers to the db
    		answ = answers(students_email=session['email'], answer_1=first_answer)
    		db.session.add(answ)
    		db.session.commit()
    	# add user answers to .json file
    	dict["answer_1"] = request.form['hiddeninput_delete']
    	file_name = session['email']+'.json'
    	with open(file_name, 'w') as fp:
    		json.dump(dict, fp, indent = 4)
    return render_template('form_submit.html', answ=answ)

# show all users -> this method is for debugging
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
		answ = answers.query.filter_by(students_email=session['email']).first()
		return render_template('form_submit.html', answ=answ)

# compiler results
@app.route('/survey/results.html')
def results():
	if ('email' in session):
		answer = answers.query.filter_by(students_email=session['email']).first()
		# dictionary with user's answers from the database
		answ = {'answer_1' : answer.answer_1}
		filename = 'NoteEditor.java'
		java_file_complete = glue_answer(filename, answ)
		file_path = 'NotePad/src/com/example/android/notepad'
		with open("%s/%s" % (file_path, filename), 'w') as f:
			f.write("%s" % java_file_complete)
		with Popen(['bash', 'compile.sh'], stdout = PIPE, stderr = PIPE, \
				universal_newlines = True) as p:
			try:
				outs, errs = p.communicate(timeout = 5)
			except TimeoutExpired:
				p.kill()
				outs, errs = p.communicate()
			# Substitute references to real methods with fake methods
			compile_out = replace_methods(outs)
			# Format newlines for basic html appearance
			compile_out = compile_out.replace('\n', '<br />')
			return render_template('results.html', answ=compile_out)

@app.route('/logout.html')
def logout():
	if 'email' not in session:
		return redirect(url_for('index'))

	session.pop('email', None)
	return render_template('logout.html')

@app.route('/survey/help.html')
def help():
	return render_template('help.html')

@app.route('/survey/api.html')
def api():
	return render_template('api.html')

if __name__ == '__main__':
   db.create_all()
   app.run(host='0.0.0.0', debug = True)

# vim: tabstop=8 noexpandtab shiftwidth=8 softtabstop=0
