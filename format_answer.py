#!/usr/bin/python
import re
from bs4 import BeautifulSoup

def format_answer(answer):
	answ = ""
	an = ""
	an = answer
	if re.search("&nbsp;", answer):
		an = re.sub("&nbsp;", " ", answer)
	elif re.search(u'\xa0', answer):
		an = re.sub(u'\xa0', " ", answer)
	answ = re.sub("[\s\n\r\t]{2,}", "", an)
	#answ = re.sub("[\s\n\r\t]{2,}", "", answer)
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
	#print (answ)
	return answ
