#!/usr/bin/python3

'''
(Attempt to) parse an `.obj` file.

Because I'm not 100% sure about the file format (and 100% of what I
know is obtained by guessing), something may be wrong.

All `assert`ions in this code are based on my knowledge. If it fails
I will change the file, not the `.obj` files.
'''

import io
import sys
from xxd import xxd

def to_int(data):
	''' Convert `bytes` to integer. (base 256) '''
	return to_int(data[1:])<<8|data[0] if data else 0
def to_str(data):
	''' `data` is a `bytes` object.
	Convert from return type of `read_str` to a `str`. '''
	return data[1:].decode('latin-1')

class BytesIO_ (io.BytesIO): 
	def readable(self):
		''' Actually this checks for not EOF. 
		Abuse of derived class ...? '''
		return len(self.getbuffer()) != self.tell()

	def read(self, size = -1):
		''' Throw EOFError when cannot read. '''
		result = io.BytesIO.read(self, size)
		if len(result) < size:
			raise EOFError()
		return result

	def read1(self):
		return self.read(1)[0]

	def read_str(self):
		'''Result contains the string length as its first byte.'''
		str_len = self.read(1)
		str_data = self.read(str_len[0])
		assert len(str_data) == str_len[0]
		return str_len + str_data

	def read_int(self, size = 2):
		return to_int(self.read(size))

	def skip_zero(self, size):
		assert self.read(size) == b'\x00'*size, xxd(self.getbuffer())

# allow user to override `print` function
def parse_data(data, print = print, parse_0x08 = False):
	data = BytesIO_(data)
	nameof_export = {} # the '_' names (public), not '$$' names.
	typeof_export = {} # the '_' names (public), not '$$' names.
	nameof_defvar = {}
	nameof_dcl    = {}
	obj_data      = {} # function code + constant values

	# Symbols in output: '#': id (something the assembler uses
	# to distinguish functions, numbered from 1), '@': address

	while data.readable():
		block_type = data.read1()
		block_size = data.read_int()
		block = data.read(block_size)

		# print(f'Block: type {hex(block_type)}, size '
		# 	+f'{hex(block_size)}, sum {hex(sum(block))}')

		block_checksum = block[-1]
		block = BytesIO_(block[:-1])

		if block_type in (0x2, 0x3): # 'abs' use 0x3... why?
			# Header, appear first
			asm_name = block.read_str()
			print(f'Name: {to_str(asm_name)}')
			assert block.read(2) == b'\x04\x01'
			print(f'Model: {to_str(block.read_str())}')
			assert block.read(1) == b'\x01', xxd(block.getbuffer())
			block.read(1)
			assert block.read(4) == b'\x01\x04\x03\x01', xxd(block.getbuffer())
			block.skip_zero(1)
			block.read(3)
			block.skip_zero(2)

		elif block_type == 0x80:
			# this block contains info about ROM window etc.
			block.read()
			pass

		elif block_type == 0x20:
			assert asm_name == block.read_str()
			assert block.read(1) == b'\x02'
			block.skip_zero(4)

		elif block_type == 0xe: 
			# fn id, size and name
			# (name is prefixed with '$$' for some reason)
			print('Functions/constants/var#')

			'''
			Some information about 'var#'.
			I have not completely decoded it, but it's related to 
			static or pre-initialized variables.
			$$NVARmain | $$NINITVAR | $$NINITTAB

			Most things about it is not known.
			'''

			# everything with storage in .OBJ
			while block.readable():
				block.skip_zero(1)
				obj_id = block.read_int()
				byte_3 = block.read1()

				# TODO xgetmem_f. XFCOD is breaking everything
				block.read1() 
				block.skip_zero(0x07)
				byte_c = block.read1()
				block.skip_zero(0x05)

				if byte_3 == 0x05:
					if   byte_c == 0x02:
						obj_type = 'const'
					elif byte_c == 0x00:
						obj_type = 'var#'
					else: assert False
				elif byte_3 == 0x00:
					obj_type = 'fn'
					assert byte_c == 0x00
				elif byte_3 == 0x01:
					obj_type = 'var#'
					assert byte_c in (0x00, 0x02), byte_c
				else:
					assert False, byte_3

				obj_size = block.read_int()
				assert block.read(0x05) == b'\x00\x00\x01\x00\x00'
				obj_name = block.read_str()

				obj_data[obj_id] = bytearray(b'\x00') * obj_size
				print(f'  {obj_type} {to_str(obj_name)}, #{obj_id}, '+
					f'size {obj_size}')

		elif block_type == 0x17:
			print('Global variables')
			while block.readable():
				block.skip_zero(1)
				var_id = block.read_int()
				assert block.read(1) == b'\x01'
				block.skip_zero(2)
				assert block.read(1) == b'\x02'
				block.skip_zero(5)
				var_adr = block.read_int()
				block.skip_zero(2)
				nameof_defvar[var_id] = to_str(block.read_str())

				print(f'  {nameof_defvar[var_id]}, #{var_id}, '+
					f'@{var_adr}')

		elif block_type == 0x16: 
			# info about symbol name <-> id
			# (symbol name) = '_' + (function name)
			while block.readable():
				block.skip_zero(1)
				obj_id = block.read_int()
				byte_3 = block.read1()
				block.skip_zero(0x03)
				byte_7 = block.read1()

				block.skip_zero(0x01)
				block.read1() # TODO 0x2e if _vsprintf_nn, else 0
				block.read1() # TODO 0x01 if __Ctype, else 0
				block.skip_zero(0x02)
				obj_name = block.read_str()

				if   byte_3 == 0x05:
					assert byte_7 in (0x02, 0x00), byte_7 # TODO
					obj_type = 'const'
				elif byte_3 == 0x00:
					assert byte_7 == 0x00, (byte_3, byte_7)
					obj_type = 'fn'
				elif byte_3 == 0x01:
					assert byte_7 == 0x02, (byte_3, byte_7)
					obj_type = 'var#'
				else:
					assert False, byte_3

				nameof_export[obj_id] = to_str(obj_name)
				typeof_export[obj_id] = obj_type
				print(f'{obj_type} {to_str(obj_name)}, #{obj_id}')

		elif block_type == 0x18:
			print('Dcl fn/extern var:')
			while block.readable():
				block.skip_zero(1)
				obj_id = block.read_int()
				obj_type = block.read1()
				obj_access = block.read1() # 00: far, 02: near
				block.skip_zero(1)
				obj_name = block.read_str()

				if   obj_type == 0x00:
					obj_typestr = 'fn'
				elif obj_type == 0x01:
					obj_typestr = 'var'
				elif obj_type == 0x05:
					obj_typestr = 'var const'
				else:
					assert False, (xxd(block.getbuffer()), obj_type)

				obj_typestr += ' '
				if   obj_access == 0x00:
					obj_typestr += 'far'
				elif obj_access == 0x02:
					obj_typestr += 'near'
				else: assert False

				nameof_dcl[obj_id] = to_str(obj_name)
				print(f'  {obj_typestr} {to_str(obj_name)}, #{obj_id}')


		elif block_type == 0x06:
			# function code/const segment
			block.skip_zero(1)
			start_address = block.read_int()
			block.skip_zero(2)
			obj_id   = block.read_int()
			obj_type = block.read1()
			assert obj_type in (
				0x00,  # function code
				0x85,  # const
			)
			read_data = block.read()

			# AFAIK, Rasu8 order the blocks correctly
			obj_data[obj_id] \
				[start_address:start_address+len(read_data)] \
				= read_data
			# however not all parts must be initialized :/
			# especially only for XFTAB or "var#" thing.

			last_block6_id = obj_id
			print(f'Block 6 for #{obj_id}, start {start_address}, len {len(read_data)}')

		elif block_type == 0x08:
			'''
			Contains info about functions or global/extern
			variables used in the function in the 0x06 block
			right before this block.
			'''

			# currently this can't parse all types correctly.
			if not parse_0x08: continue

			print('External addresses for fn ' + 
				nameof_export[last_block6_id])
			xxd(block.getbuffer())

			while block.readable():
				call_adr = block.read_int() # offset 0
				byte_2 = block.read1()
				is_struct = byte_2&1; byte_2 ^= is_struct

				block.skip_zero(2)

				is_function = block.read1()

				# 1: deffn, 2: dclfn/extern, 3: var
				_type = block.read1() # offset 6

				_id = block.read_int() # offset 7

				byte_9 = block.read1()
				block.skip_zero(1)
				offset = block.read_int() # offset 0b
				block.skip_zero(2)

				# 0 for fn, 1 for var/extern var, 5 for extern var const
				# (for var const it's just hardcoded)
				byte_0f = block.read1() # offset 0f
				_type2 = byte_0f&0b101; byte_0f ^= _type2

				assert (byte_9>>1)&1 == (_type2 != 0)
				byte_9 &= ~2

				# Don't read this `if` statement
				if is_function == 1:
					assert not is_struct
					assert _type2 == 0
					if _type == 1:
						typestr = 'deffn'
					elif _type == 2:
						typestr = 'dclfn'
					else: assert False
				elif is_function == 0 or is_function == 0x0d:
					typestr = 'struct' if is_struct else 'var'
					if _type == 2:
						if _type2 == 1:
							typestr = f'extern {typestr}'
						elif _type2 == 5:
							typestr = f'extern {typestr} const'
						else: assert False
					elif _type == 3:
						assert _type2 == 1
						typestr = f'{typestr}'
					else: assert False
				else: assert False

				name_dict = {
					1: nameof_export, 2: nameof_dcl, 3: nameof_defvar
				}[_type]
				print(f'  call@ {call_adr}, {typestr}, ' +
					f'name {name_dict[_id]}, offset {offset}')
				if byte_2 or byte_9 or byte_0f:
					print('Warning: Partially unrecognized 0x08 subblock')
					xxd(block.getbuffer()[:block.tell()][-16:])

		elif block_type == 0x13:
			print('Source file name(s):')
			assert block.read(1) == b'\x0a'
			n_file = block.read_int()
			for file_index in range(n_file):
				assert block.read_int() == file_index
				block.read(1) # unknown, checksum or something
				block.skip_zero(3)
				print(f'  {to_str(block.read_str())}')

		elif block_type == 0x11:
			# unknown. There are multiple 0x11 blocks in an obj file.
			block.read(1)

		elif block_type == 0x22:
			# weird empty block
			pass

		elif block_type == 0x4:
			assert asm_name == block.read_str()
			block.skip_zero(2)

		else:
			print(f'Unknown block, type {hex(block_type)}')
			xxd(block.getbuffer())
			block.read()
			print('')

		assert not block.readable(), xxd(block.getbuffer())

	# at the end of the 'parse_data' function
	print('') 

	return {
		'nameof_export' : nameof_export,
		'typeof_export' : typeof_export,
		'nameof_defvar' : nameof_defvar,
		'nameof_dcl'    : nameof_dcl,
		'obj_data'      : obj_data,
	}

def main():
	if len(sys.argv) != 2:
		raise Exception(
			'Please provide 1 argument, path to an .obj file')

	with open(sys.argv[1], 'rb') as obj_file:
		parse_data(obj_file.read())

if __name__ == '__main__':
	main()
