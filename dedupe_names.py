#!/usr/bin/python

# Prefix latter redundant lines in the rename list with '#####'.
# Only handle hexadecimal address format.

import re

addr_regex = re.compile(r'[0-9a-fA-F]{4,6}\b')
names_filename = '570es+_names.txt'

out = ''
seen_addrs = set()
with open(names_filename, 'r') as f:
	content = f.read()
	for line in content.splitlines():
		addr = addr_regex.match(line)
		if addr:
			addr = addr[0].lower()
			if addr in seen_addrs:
				# redundant, comment the line out
				out += '##### '
			else:
				seen_addrs.add(addr)

		out += line + '\n'

with open(names_filename + '.bkp', 'w') as f:
	f.write(content)

with open(names_filename, 'w') as f:
	f.write(out)
