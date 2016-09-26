import re
import copy

from collections import defaultdict
from string import Template

global method_dict

# initialize the dictionary for the methods with checked exceptions such as {fake method: real method}
method_dict = {'deleteRecord' : 'delete', \
		'editText' : 'setText_new', \
		'insertData' : 'insert_new', \
		'setLayout' : 'setContentView_new', \
		'findViewId' : 'findViewById_new', \
		'changeTextColor' : 'setTextColor_new', \
		'getCursorString' : 'getString', \
		'queryData' : 'query_new', \
		'updateRecord' : 'update', \
		'drawTxt' : 'drawText_new'}

# initialize the dictionary for the methods with unchecked exceptions such as {fake method: real method}
method_dict_unchecked = {'deleteRecord' : 'delete', \
		'editText' : 'setText', \
		'insertData' : 'insert', \
		'setLayout' : 'setContentView', \
		'findViewId' : 'findViewById', \
		'changeTextColor' : 'setTextColor', \
		'getCursorString' : 'getString', \
		'queryData' : 'query', \
		'updateRecord' : 'update', \
		'drawTxt' : 'drawText'}

# answer_block is a dict of user's answers,
# i.e. answer_block = {'answer_1' : fake_answer}
# survey type refers to the different surveys 
# (methods with checked exceptions Vs. methods with unchecked exceptions--documented and undocumented)
def glue_answer(filepath, answers):
	# open the file
	filein = open(filepath)
	# read it
	src = Template(filein.read())
	# dictionary for answers with real Android's API methods
	real_answers = bind_method(answers)
	#do the substitution
	result = src.substitute(real_answers)
	return result

# Bind the answers' methods to the real Android's API methods
# answers is a dict, i.e. answers = {'answer_1' : fake_answer}
# This function returns a dict of answers with real Android's
# API methods, i.e. real_answers = {'answer_1' : real_answer}
def bind_method(answers):
	real_answers = {}
	a_keys = list(answers.keys())
	m_keys = list(method_dict.keys())
	# for each user answer
	for k, l in enumerate(a_keys):
		# get the value of the answer
		an = answers.get(a_keys[k])
		# for each fake method
		for m, n in enumerate(m_keys):
			# search for fake method in the answer
			fake = m_keys[m]
			if (re.search(fake, an)):
				#print ("find fake :" + fake)
				# get real method
				real = method_dict.get(fake)
				if (a_keys[k] not in list(real_answers.keys())):
					real_answers[a_keys[k]] = re.sub(fake+'\(', real+'(', an)
					break
	# check if finally there exists fake method in user's answer
	for d, f in enumerate(a_keys):
		if (a_keys[d] not in list(real_answers.keys())):
			real_answers[a_keys[d]] = answers.get(a_keys[d])
	return real_answers

def replace_methods(compiler_output):
	for fake, real in method_dict.items():
		#compiler_output = compiler_output.replace(fake, real)
		compiler_output = re.sub(real, fake, compiler_output)
	if re.search("\bsetTextColor\b\(\bcolors\b\)", compiler_output):
		compiler_output = re.sub("\bsetTextColor\b\(\bcolors\b\)", "changeTextColor(colors)", replace_output)
	return compiler_output

'''
def set_dict(survey_type):
	method_dict = {}
	if (survey_type == 'unchecked') or (survey_type == 'doc-unchecked'):
		method_dict = copy.deepcopy(method_dict_unchecked)
	elif (survey_type == 'checked'):
		method_dict = copy.deepcopy(method_dict_checked)
	return method_dict
'''

# vim: tabstop=8 noexpandtab shiftwidth=8 softtabstop=0
