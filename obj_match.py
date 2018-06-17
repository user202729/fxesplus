#!/usr/bin/python3

# **FAILED.**
# 'parse_obj.py' and 'extract.py' together is already too good.

import re

# `C:` for Windows users
DRIVE_C = '/home/user202729/.wine/drive_c'

# LIB file taken from U8DevTool.
lib_path = DRIVE_C + '/Program Files/U8Dev/Lib/LU8100LW.lib'

# You have to generate the LST file by running
# `LibU8 LU8100LW;` in the folder containing LIB file
lst_path = 'wine_tools/LU8100LW.lst'

with open(lst_path, 'r') as lst_file:
	lst = [line.rstrip('\r\n') for line in lst_file][::-1]
with open(lib_path, 'rb') as lib_file:
	lib = lib_file.read()

# =========== end reading input

from xxd import xxd

assert lst.pop().startswith('LIBU8 Object Librarian')
lst.pop() # The day the LST file is generated
assert not lst.pop()

assert lst.pop().upper() == 'LIBRARY FILE : LU8100LW.LIB'
module_cnt = int(lst.pop().lstrip('MODULE COUNT : '))

lib_header_size = 14 # I think it's >=13 and <=18.
lib = lib[lib_header_size:]

RT_OPCODE      = b'\x1f\xfe'
PUSH_LR_OPCODE = b'\xce\xf8'
POP_PC_OPCODE  = b'\x8e\xf2'

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

	obj_part = lib[:byte_size]
	lib = lib[byte_size:]

	print(f'Module {module_name}')
	xxd(obj_part)
	print()

	if len(symbols) > 1:
		print(f'Module {module_name} has multiple symbols')
		continue

	rt_index = obj_part.find(RT_OPCODE)
	if rt_index < 0:
		push_lr_index = obj_part.find(PUSH_LR_OPCODE)
		pop_pc_index  = obj_part.rfind(POP_PC_OPCODE)

		if push_lr_index < 0 or pop_pc_index < 0:
			print(f'Weird module: {module_name} (no fn)')
			continue

			# obj_part.find(b'\x8e\xf2', pop_pc_index +1) >= 0
	else:
		if obj_part.find(RT_OPCODE, rt_index+1) >= 0:
			print(f'Weird module: {module_name} (have >1 rt)')


assert all(not x for x in lst)

# The remaining bytes (those left in (lib) now) are probably data
# types, calling convention, etc.
