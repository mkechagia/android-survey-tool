from flask import Flask, request, flash, url_for, redirect, render_template, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from signup import SignupForm
from models import app, db, students, answers
import validators
from validators import email
import os
from sqlalchemy import update
from collections import defaultdict
from subprocess import Popen, PIPE, TimeoutExpired
from glue import glue_answer, replace_methods
import format_answer
import re

global answ
answ = {}

@app.route('/')
def index():
   return render_template('index.html')

# Add new user's (i.e. student) details to the database
@app.route('/new', methods = ['GET', 'POST'])
def new():
	if (request.method == 'POST'):
		if (not request.form['email'] or not request.form['password'] or not request.form['secret'] or not request.form['job'] or not request.form['code'] or not request.form['android']):
			flash('Please enter all the fields and update the selection boxes.', 'error')
		else:
			student = students(email = request.form['email'], password=request.form['password'], secret=request.form['secret'], job=request.form['job'], code=request.form['code'], android=request.form['android'])
			# check if the email already exists---unique user
			if (not db.session.query(students.id).filter(students.email == student.email).count() == 0):
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
					# create a new answer
					answ = answers(students_email = session['email'], \
						answer_1 = '// There is no answer yet. Please press Clear and give your answer.', \
						answer_2 = '// There is no answer yet. Please press Clear and give your answer.',
						answer_3 = '// There is no answer yet. Please press Clear and give your answer.', \
						answer_4 = '// There is no answer yet. Please press Clear and give your answer.',
						answer_5 = '// There is no answer yet. Please press Clear and give your answer.', \
						answer_6 = '// There is no answer yet. Please press Clear and give your answer.',
						answer_7 = '// There is no answer yet. Please press Clear and give your answer.', \
						answer_8 = '// There is no answer yet. Please press Clear and give your answer.',
						answer_9 = '// There is no answer yet. Please press Clear and give your answer.', \
						answer_10 = '// There is no answer yet. Please press Clear and give your answer.')
					db.session.add(answ)
					db.session.commit()
					# get answer with session's email
					answ = answers.query.filter_by(students_email = session['email']).first()
					return render_template('form_submit.html', answ = answ)
				else:
					flash('The email is not valid.', 'error')
	return render_template('new.html')

# Define a route for the action of the form, for example '/survey/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/survey/', methods=['POST'])
def survey():
    if ('email' in session):
    	# find answers of the user with the email in the session
    	answ = answers.query.filter_by(students_email = session['email']).first()
    	# format user's answer; request.form based on the name of the textarea
    	first_answer = format_answer.format_answer(request.form['t_answer_1'])
    	second_answer = format_answer.format_answer(request.form['t_answer_2'])
    	a3_answer = format_answer.format_answer(request.form['t_answer_3'])
    	a4_answer = format_answer.format_answer(request.form['t_answer_4'])
    	a5_answer = format_answer.format_answer(request.form['t_answer_5'])
    	a6_answer = format_answer.format_answer(request.form['t_answer_6'])
    	a7_answer = format_answer.format_answer(request.form['t_answer_7'])
    	a8_answer = format_answer.format_answer(request.form['t_answer_8'])
    	a9_answer = format_answer.format_answer(request.form['t_answer_9'])
    	a10_answer = format_answer.format_answer(request.form['t_answer_10'])
    	# update user's answers to the db
    	answ.answer_1 = first_answer
    	answ.answer_2 = second_answer
    	answ.answer_3 = a3_answer
    	answ.answer_4 = a4_answer
    	answ.answer_5 = a5_answer
    	answ.answer_6 = a6_answer
    	answ.answer_7 = a7_answer
    	answ.answer_8 = a8_answer
    	answ.answer_9 = a9_answer
    	answ.answer_10 = a10_answer
    	db.session.commit()
    	# get user's current aswers
    	answ = answers.query.filter_by(students_email = session['email']).first()
    	# It is better to also add this when press compile TO-DO: remaining answers
    	if re.search("//", first_answer) or re.search("//", second_answer) or re.search("//", a3_answer):
    		flash('Please fill all the answer boxes.', 'error')
    return render_template('form_submit.html', answ = answ)

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
		# get answers for the email in the session
		answ = answers.query.filter_by(students_email = session['email']).first()
		return render_template('form_submit.html', answ = answ)

# compiler results
@app.route('/survey/results.html')
def results():
	if ('email' in session):
		answer = answers.query.filter_by(students_email=session['email']).first()
		# dictionary with user's answers from the database
		answ = {'answer_1' : answer.answer_1, 'answer_2' : answer.answer_2, \
				'answer_3' : answer.answer_3, 'answer_4' : answer.answer_4, \
				'answer_5' : answer.answer_5, 'answer_6' : answer.answer_6, \
				'answer_7' : answer.answer_7, 'answer_8' : answer.answer_8, \
				'answer_9' : answer.answer_9, 'answer_10' : answer.answer_10}
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
