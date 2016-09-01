import os
import re

def format_answer(answer):
	return re.sub("{", '{\n', answer)