import re

from collections import defaultdict

from string import Template

global method_dict
# initialize the dictionary such as {fake method: real method}
method_dict = {'getContentResolver().deleteRecord(mUri, null, null)' : 'getContentResolver().delete(mUri, null, null)'}
# dictionary for answers with real Android's API methods
global real_answers
real_answers = {}

# Glue user's answers to the NoteEdit.java
# answer_block is a dict of user's answers, i.e. answer_block = {'answer_1' : fake_answer}
def glue_answer(filepath, answer_block):
	#open the file
	filein = open(filepath)
	#read it
	src = Template(filein.read())
	#do the substitution
	real_answers = bind_method(answer_block)
	# Marios: TODO: as I wrote in routes.py we need a dict
	# of answers to substitute and this should not happen here
	# as is the case now. The answer_block argument to this
	# function should already be a dict, i.e. {'answer_1': real_answer}
	# Maria: TO-DO: check if the substitute method works with the dictionary now
	result = src.substitute(real_answers)
	return result

# Bind the answers' methods to the real Android's API methods
# answers is a dict, i.e. answers = {'answer_1' : fake_answer}
# This function returns a dict of answers with real Android's API methods, i.e. real_answers = {'answer_1' : real_answer} 
def bind_method(answers):
	real_answers = {}
	a_keys = list(answers.keys())
	m_keys = list(method_dict.keys())
	# process each answer
	for d, f in enumerate(a_keys):
		answer = answers.get(a_keys[d])
		for l, m in enumerate(m_keys):
			if (answer.find(m_keys[l])):
				real_answers[a_keys[d]] = answer.replace(m_keys[l], method_dict.get(m_keys[l]))
				break
			else:
				real_answers[a_keys[d]] = answer
	return real_answers


# vim: tabstop=8 noexpandtab shiftwidth=8 softtabstop=0
