from flask import Flask, request, flash, url_for, redirect, render_template, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from signup import SignupForm
from flask_wtf import Form
from wtforms import validators
from wtforms.fields.html5 import EmailField
from models import app, db, students, answers, timestamps, submissions
#import validators
from validators import email
#from wtforms.validators import Required
#from wtforms.validators import email
import os
from sqlalchemy import update
from sqlalchemy import func
from collections import defaultdict
from subprocess import Popen, PIPE, TimeoutExpired
from glue import glue_answer, replace_methods
import format_answer
import random
import re
from datetime import datetime
# obtain a connection to a database 
from sqlalchemy import create_engine
e = create_engine('sqlite:///students.sqlite3')

global answ
answ = {}
global form_list
form_list = ['t_answer_1', 't_answer_2', 't_answer_3', 't_answer_4', 't_answer_5', 't_answer_6', \
				't_answer_7']

@app.route('/static/stylesheet.css')
def serve_static_css(filename):
	root_dir = os.path.dirname(os.getcwd())
	return send_from_directory(os.path.join(root_dir, 'static', 'css'), filename)

@app.route('/static/script.js')
def serve_static_js(filename):
	root_dir = os.path.dirname(os.getcwd())
	return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/new', methods = ['GET', 'POST'])
def new():
	answ = ""
	if (request.method == 'POST'):
		if (not request.form['email'] or not request.form['password'] or not request.form['password_2'] or not request.form['education'] or not request.form['company'] or not request.form['job'] or not request.form['code'] or not request.form['java'] or not request.form['android']):
			flash('Please fill all the fields and selection boxes.', 'error')
		elif (request.form['password'] != request.form['password_2']):
			flash('Your passwords should be the same.', 'error')
		else:
			student = students(email = request.form['email'], password=request.form['password'], education=request.form['education'], company=request.form['company'], job=request.form['job'], code=request.form['code'], java=request.form['java'], android=request.form['android'])
			# check if the email already exists---unique user
			if (not db.session.query(students).filter(students.email == student.email).count() == 0):
				# check that we are in the sign up page
				if ('email' not in session):
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
					# timestamp
					now = datetime.utcnow()
					# create a new answer
					answ = answers(students_email = session['email'], timestamp = now, \
						answer_1 = '', \
						answer_2 = '', \
						answer_3 = '', \
						answer_4 = '', \
						answer_5 = '', \
						answer_6 = '', \
						answer_7 = '')
					db.session.add(answ)
					db.session.commit()
					# get answer with session's email
					answ = answers.query.filter_by(students_email = session['email']).first()
					return render_template(set_survey_type(get_rowid(session['email'])), answ = answ)
				else:
					flash('The email is not valid.', 'error')
	if ('email' in session):
		# find answers of the user with the email in the session
		answ = answers.query.filter_by(students_email = session['email']).first()
		return render_template(set_survey_type(get_rowid(session['email'])), answ = answ)
	else:
		return render_template('new.html')

# Define a route for the action of the form, for example '/survey/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/survey/', methods=['POST'])
def survey():
	if ('email' in session):
		# list for the formated answers from the survey form
		formatted_answers = []
		# find answers of the user with the email in the session
		answ = answers.query.filter_by(students_email = session['email']).first()
		# update the timestamp
		now = datetime.utcnow()
		answ.timestamp = now
		# format user's answer; request.form based on the name of the textarea
		for k, l in enumerate(form_list):
			# format user's answer; request.form based on the name of the textarea
			formatted_answer = format_answer.format_answer(request.form[form_list[k]])
			formatted_answers.append(formatted_answer)
		# add formatted answers to the db
		answ.answer_1 = formatted_answers[0]
		answ.answer_2 = formatted_answers[1]
		answ.answer_3 = formatted_answers[2]
		answ.answer_4 = formatted_answers[3]
		answ.answer_5 = formatted_answers[4]
		answ.answer_6 = formatted_answers[5]
		answ.answer_7 = formatted_answers[6]
		# commit timestamp and all user's answers to the db
		db.session.commit()
		# get user's current aswers
		answ = answers.query.filter_by(students_email = session['email']).first()
		# check for empty answer boxes when format
		for d, f in enumerate(formatted_answers):
			if (formatted_answers[d] == ''):
				flash('Please fill answer box '+str(d+1)+'.', 'error')
	return render_template(set_survey_type(get_rowid(session['email'])), answ = answ)

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
		return render_template(set_survey_type(get_rowid(session['email'])), answ = answ)

# compiler results
@app.route('/survey/results.html')
def results():
	srv_type = ''
	page = ''

	if ('email' in session):

		# set the survey type based on the kind of the survey's main page
		page = set_survey_type(get_rowid(session['email']))
		if page == 'form_submit_ct.html':
			srv_type = 'checked'
		elif page == 'form_submit_rt.html':
			srv_type = 'unchecked'

		# get answers for the email in the session
		answer = answers.query.filter_by(students_email=session['email']).first()
		# dictionary with user's answers from the database
		answ = {'answer_1' : answer.answer_1, 'answer_2' : answer.answer_2, \
				'answer_3' : answer.answer_3, 'answer_4' : answer.answer_4, \
				'answer_5' : answer.answer_5, 'answer_6' : answer.answer_6, \
				'answer_7' : answer.answer_7}

		# check for empty answer boxes
		if (check_answer_boxes(answ)):
			filename = 'NoteEditor.java'
			java_file_complete = glue_answer(filename, answ, srv_type, session['email'])
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
				compile_out = replace_methods(outs, srv_type)
				# Format newlines for basic html appearance
				compile_out = compile_out.replace('\n', '<br />')
				compile_out += "<br><a href=\"../static/%s-NoteEditor.java\", target=\"_blank\">View source code</a>" % (session['email'])
				
				# answers to string
				str_answers = answers_to_str(answer)
				# store submission and compile output to the db
				store_submission_output(session['email'], str_answers, outs)

				return render_template('results.html', answ=compile_out)
		else:
			# if there are empty answer boxes
			compile_out = "Please fill all the answer boxes."
			return render_template('results.html', answ=compile_out)

@app.route('/logout.html')
def logout():
	if 'email' not in session:
		return redirect(url_for('index'))

	session.pop('email', None)
	return render_template('logout.html')

@app.route('/survey/help.html')
def help():
	if ('email' in session):
		set_timestamp(session['email'], 'help.html')
	return render_template('help.html')

@app.route('/survey/api/')
def api():
	if ('email' in session):
		page = ""
		rowid = 0
		# find student's rowid for returning different API pages
		rowid = get_rowid(session['email'])

		# case for checked exceptions
		if (int(float(rowid)) % 3 == 0):
			page = 'api-explore-doc.html'
		# case for documented and unchecked exceptions (to-be)
		elif (int(float(rowid)) % 2 == 0):
			page = 'api-explore.html'
		# case for undocumented and unchecked exceptions (as-is)
		else:
			page = 'api-android.html'

		# store timestamp of the visited page to the db
		set_timestamp(session['email'], page)

		return render_template(page)

# AS-IS Android documentation (undocumented and unchecked exceptions)
@app.route('/api-android/', defaults={'path': ''})
@app.route('/<path:path>')
def api_android(path):
	if ('email' in session):
		set_timestamp(session['email'], path)
	return render_template(path)

# TO-BE Android documentation (documented and unchecked exceptions)
@app.route('/api-explore/', defaults={'path': ''})
@app.route('/<path:path>')
def api_explore(path):
	if ('email' in session):
		set_timestamp(session['email'], path)
	return render_template(path)

# TO-BE Android documentation (checked exceptions)
@app.route('/api-explore-doc/', defaults={'path': ''})
@app.route('/<path:path>')
def api_explore_doc(path):
	if ('email' in session):
		set_timestamp(session['email'], path)
	return render_template(path)

# get student's rowid for setting survey type
# (box with different exceptions and API documentation per case)
def get_rowid(st_email):
	rowid = 0
	for row in e.execute('SELECT rowid FROM students WHERE email=?', st_email):
		rowid = row[0]
	return rowid

# set survey type (for the exceptions' box---main survey page)
def set_survey_type(rowid):
	page = ''
	# case for checked exceptions
	if (int(float(rowid)) % 3 == 0):
		page = 'form_submit_ct.html'
		return page # page with checked exceptions
	else:
		page = 'form_submit_rt.html'
		return page # page with unchecked exceptions

# store timestamp to the db
def set_timestamp(session_email, visited_page):
	now = datetime.utcnow()
	t = timestamps(email = session_email, page = visited_page, timestamp = now)
	db.session.add(t)
	db.session.commit()

# check for empty answer boxes
def check_answer_boxes(answ_dict):
	res = True
	an_keys = list(answ_dict.keys())
	for d, f in enumerate(an_keys):
		if (answ_dict.get(an_keys[d]) == ''):
			res = False
	return res

# store submission and compile output to the db
def store_submission_output(session_email, answers, out):
	counter = 0
	# for the timestamp
	now = datetime.utcnow()

	# add new record - submission to the db
	submission = submissions(email = session_email, count_submission = counter, timestamp = now, answer = answers, output = out)
	db.session.add(submission)
	db.session.commit()

	# get the number of the submissions per user until now
	counter = db.session.query(submissions).filter(submissions.email == session_email).count()
	# update the counter of the record
	submission.count_submission = counter
	db.session.commit()
	
# return answer record to string
def answers_to_str(answer):
	an = ""
	an_1 = "answer 1: " + answer.answer_1
	an_2 = "answer 2: " + answer.answer_2
	an_3 = "answer 3: " + answer.answer_3
	an_4 = "answer 4: " + answer.answer_4
	an_5 = "answer 5: " + answer.answer_5
	an_6 = "answer 6: " + answer.answer_6
	an_7 = "answer 7: " + answer.answer_7
	an = (an_1+", "+an_2+", "+an_3+", "+ an_4+", "+an_5+", "+an_6+", "+an_7)
	return an

if __name__ == '__main__':
   db.create_all()
   app.run(host='0.0.0.0', debug = True)

# vim: tabstop=8 noexpandtab shiftwidth=8 softtabstop=0