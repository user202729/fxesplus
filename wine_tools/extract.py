#!/usr/bin/python3

# Extract `.obj` files from `.lib` file. Place the result in `./obj/`.
# You may pass a parameter to specify the library file name.
# (with or without '.lib' are both ok)

CMD = 'wine cmd'
# LIB file. Should be placed in the current directory.
lib_name = 'LU8100LW'

import re
import os
import sys

if len(sys.argv) == 2:
	lib_name = sys.argv[1]
	if lib_name.lower().endswith('.lib'):
		lib_name = lib_name[:-4]

os.system(f'{CMD} /c "init && LibU8 {lib_name};"') # extract LST file
os.system(f'{CMD} /c "rd /s /q obj & mkdir obj"')

with open(f'{lib_name}.lst', 'r') as lst_file:
	lst = [line.rstrip('\r\n') for line in lst_file][::-1]

# =========== end reading input

sys.path.append('..')
from xxd import xxd

assert lst.pop().startswith('LIBU8 Object Librarian')
lst.pop() # The day the LST file is generated
assert not lst.pop()

assert lst.pop().upper() == f'LIBRARY FILE : {lib_name.upper()}.LIB'
module_cnt = int(lst.pop().lstrip('MODULE COUNT : '))

modules = []
for _ in range(module_cnt):
	for _ in range(3): # 3 empty lines
		assert not lst.pop()

	module_name = re.sub(r'MODULE NAME *: (.*?) *$', r'\1', lst.pop())
	assert lst.pop().startswith('DATE')
	byte_size = int(re.sub(r'BYTE SIZE *: .*\((.*)\)', r'\1', lst.pop()))
	assert byte_size
	assert lst.pop().startswith('MEMORY MODEL')
	assert lst.pop().startswith('TRANSLATOR')
	assert lst.pop().startswith('CORE ID')
	assert lst.pop().startswith('TARGET')
	assert not lst.pop()
	assert lst.pop() == '==== PUBLIC SYMBOLS ===='
	assert not lst.pop()
	symbols = lst.pop().split()

	modules.append(module_name)

assert all(not x for x in lst)

os.system(f'{CMD} /c "init && \
	LibU8 {lib_name} '+' '.join('*obj\\'+x for x in modules)+';"')

