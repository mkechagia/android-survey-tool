import re

from collections import defaultdict

from string import Template

global method_dict
# initialize the dictionary
# Marios: I changed the method mapping. I thought {fake : real} was more rational
method_dict = {'getContentResolver().deleteRecord(mUri, null, null)' : 'getContentResolver().delete(mUri, null, null)'}

# For each given answer by the user
def glue_answer(filepath, answer_block):
	#open the file
	filein = open(filepath)
	#read it
	src = Template(filein.read())
	#do the substitution
	real_answer = bind_method(answer_block)
	# Marios: TODO: as I wrote in routes.py we need a dict
	# of answers to substitute and this should not happen here
	# as is the case now. The answer_block argument to this
	# function should already be a dict
	result = src.substitute({'answer_1': real_answer})
	#result = src.substitute(bind_method(answer_block))
	return result

# Bind the answer to the real Android method
def bind_method(answer):
	answ = ""
	m_keys = list(method_dict.keys())
	for l, m in enumerate(m_keys):
		if (answer.find(m_keys[l])):
			answ = answer.replace(m_keys[l], method_dict.get(m_keys[l]))
			break
		else:
			answ = answer
	return answ


# vim: tabstop=8 noexpandtab shiftwidth=8 softtabstop=0
