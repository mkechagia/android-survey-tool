#!/usr/bin/python
import re

def format_answer(answer):
	answ = ""
	# exclude the initial comment
	if (not re.search("//", answer)):
		answ = re.sub("[\s\n\r\t]*", "", answer)
		if re.search('{', answ):
			answ = re.sub("{", " {\n\t", answ)
		if re.search(';', answ):
			answ = re.sub(";", ";\n\t", answ)
		if re.search('[\s\t]*}catch', answ):
			answ = re.sub("[\s\t\r\n]*}catch", "\n} catch", answ)
		if re.search('[\s\t\r\n]*}', answ):
			answ = re.sub("[\s\t\r\n]*}", "\n}", answ)
		if re.search('catch\(', answ):
			answ = re.sub(r'catch\(', "catch (", answ)
		if re.search(',', answ):
			answ = re.sub("," , ", ", answ)
		if re.search('aExc', answ):
			answ = re.sub("aExc" , " aExc", answ)
	else:
		answ = answer
	return answ
