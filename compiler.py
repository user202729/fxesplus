import re
import sys

from lib_570esp import *

def canonicalize(st):
	''' Make (st) canonical. '''
	st = st.lower()
	st = st.strip()
	# remove spaces around non alphanumeric
	st = re.sub(r' *([^a-z0-9]) *', r'\1', st)
	return st

def get_commands(filename = 'builtins'):
	commands = {}

	file = open(filename, 'r')
	data = file.read().split('\n')
	file.close()

	in_comment = False
	for line_index, line in enumerate(data):
		line = line.strip()

		# multi-line comments
		if line == '/*':
			in_comment = True
			continue
		if line == '*/':
			in_comment = False
			continue
		if in_comment:
			continue

		# inline comments
		i = line.find('#')
		if i >= 0: line = line[:i]
		line = line.strip()
		if not line: # if it's empty
			continue

		try:
			address, command = line.split('\t')
		except ValueError:
			raise Exception(f'Line {line_index} has too many tab characters')

		command = canonicalize(command)

		tags = [] # process tags (leading `{...}`)
		while command and command[0] == '{':
			i = command.find('}')
			if i < 0:
				raise Exception(f'Line {line_index} has unmatched "{{"');
			tags.append(command[1:i])
			command = command[i+1:]

		if not command:
			raise Exception(f'Line {line_index} has empty command')

		if command in commands:
			raise Exception(f'Command f{command} appears twice - second occurence on line {line_index}')

		commands[command] = (int(address, 16), tuple(tags))

	return commands


# print symbols in table form

colwidth = max(map(len,symbols)) + 1
for i in range(256):
	print(symbols[i].ljust(colwidth), end='')
	if i % 16 == 15: print()


