import os
import json

from collections import defaultdict
from string import Template

global d
d = {}

def main():
	java_path = "/Users/marki/Desktop/test_env/NoteEditor.java.txt"
	json_path = "/Users/marki/Desktop/test_env/mariakex_sal@yahoo.gr.json"
	read_java(java_path, json_path)

def read_java(java_path, json_path):	
	#open the file
	filein = open(java_path)
	#read it
	src = Template( filein.read() )
	# decode json file to dictionary
	#d = decode_json_doc(json_path)
	d = {"answer_1": "\r\n                    \r\n                    \r\n                    \r\n                    \r\n                    \r\n                    \r\n                    try\u00a0{\u00a0}\u00a0\r\n                    \r\n                    \r\n                    \r\n\r\n                    \r\n                \r\n                    catch\u00a0\r\n                    \r\n                    \r\n                    \r\n\r\n                    \r\n                \r\n                    try\u00a0\r\n                    \r\n                    \r\n                    \r\n\r\n                    \r\n                \r\n                    catch\u00a0\r\n                    \r\n                    \r\n                    \r\n\r\n                    \r\n                \r\n                    \r\n                    try\u00a0\r\n                    \r\n                    \r\n\r\n                    \r\n                \r\n                    \r\n                    try\u00a0{\u00a0\r\n                    \r\n                    \r\n\r\n                    \r\n                "}
	#do the substitution
	result = src.substitute(d)
	print len(d)
	
# decode json files into dictionary
def decode_json_doc(json_path):
	with open(json_path) as f:
		return json.load(f)

if __name__ == "__main__":
		main()