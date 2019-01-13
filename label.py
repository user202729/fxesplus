#!/usr/bin/python

# Useful while resolving jumptable manually.
# Tries to automatically name functions in a jump table using
# information in the rename list.
# Usage: Input (list of hexadecimal address) on stdin,
# output is appended to the rename list.

import re, sys

names_filename = '570es+_names.txt'

with open(names_filename, 'r') as f:
	names = f.read().splitlines()

out = ''

addr_regex = re.compile(r'[0-9a-fA-F]+')
content = sys.stdin.read()

for line in content.splitlines():
	addr = addr_regex.match(line)
	if not addr:  # comment line, output literally
		out += line + '\n'
		continue

	for name in names:
		if name.lower().startswith(line.lower()):  # perfect match
			out += name + '\n'
			break

	else:
		addr = addr[0].lower()
		for name in names:
			if name.lower().startswith(addr):  # partial match
				out += line + '\n'
				out += '\t\t\t## ' + name + '\n'
				break

		else:  # no match
			out += line + '\n'

with open(names_filename, 'a') as f:
	f.write(out)
