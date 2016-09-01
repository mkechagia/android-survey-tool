import os
import json

from collections import defaultdict
from string import Template

def glue_answer(answer_block):
	#open the file
	filein = open("NoteEditor.java")
	#read it
	src = Template( filein.read() )
	#do the substitution
	result = src.substitute(answer_block)
	return result
