#!/usr/bin/python3

CMD = 'wine cmd'
# LIB file. Should be placed in the current directory.
lib_name = 'LU8100LW'

import re
import os

os.system(f'{CMD} /c "init && LibU8 {lib_name};"') # extract LST file
os.system(f'{CMD} /c "rd /s /q obj & mkdir obj"')

with open(f'{lib_name}.lst', 'r') as lst_file:
	lst = [line.rstrip('\r\n') for line in lst_file][::-1]

# =========== end reading input

def xxd(data):
	hex_data = [hex(byte)[2:].zfill(2) for byte in data]
	ascii_data = [
		chr(byte) if 0x20<=byte<=0x7E else '.'
		for byte in data]

	# pad to multiple of 16
	rem = (-len(data))%16
	hex_data.extend(['  '] * rem)
	ascii_data.extend([' '] * rem)

	ascii_data = ''.join(ascii_data)

	for addr in range(0, len(hex_data), 16):
		print(hex(addr)[2:].zfill(4), end=': ')
		for i in range(0, 16, 2):
			print(''.join(hex_data[addr+i:addr+i+2]),end=' ')
		print('  '+ascii_data[addr:addr+16])

assert lst.pop().startswith('LIBU8 Object Librarian')
lst.pop() # The day the LST file is generated
assert not lst.pop()

assert lst.pop().upper() == 'LIBRARY FILE : LU8100LW.LIB'
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

