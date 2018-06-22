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
		zero_data = self.read(size)
		assert zero_data == b'\x00'*size, (
			xxd(zero_data), print('===='), xxd(self.getbuffer()))

	def xxd(self):
		xxd(self.getbuffer())

def access_spec(_access):
	'''
	Get object access specification as a string ('near' or 'far')
	0x00: far, 0x02: near.
	'''
	if   _access == 0x00:
		return 'far'
	elif _access == 0x02:
		return 'near'
	else: assert False

def get_type(_type):
	'''
	Get object type as a string.
	* 0x00: 'fn'    (function)
	* 0x01: 'var'   (variable)
	* 0x05: 'const' (constant)
	'''
	if   _type == 0x05:
		return 'const'
	elif _type == 0x00:
		return 'fn'
	elif _type == 0x01:
		return 'var'
	else:
		assert False, _type

# allow user to override `print` function
def parse_data(data, print = print, parse_0x08 = False):
	data = BytesIO_(data)
	nameof_export = {} # the '_' names (public), not '$$' names.
	typeof_export = {}
	nameof_defvar = {}
	nameof_dcl    = {}
	obj_data      = {} # function code + constant values

	# Symbols in output: '#': id (something the assembler uses
	# to distinguish functions, numbered from 1), '@': address

	while data.readable():
		block_type = data.read1()
		block_size = data.read_int()
		block = data.read(block_size)

		# print(f'Block: type {hex(block_type)}, size {block_size}')

		assert (sum(block) + block_type +
			(block_size & 0xFF) + (block_size >> 8)) & 0xFF == 0

		# this byte is only included for calculating checksum
		block_checksum = block[-1]
		block = BytesIO_(block[:-1])

		if block_type in (0x2, 0x3): # 'abs' use 0x3... why?
			# Header, appear first
			asm_name = block.read_str()
			print(f'Name: {to_str(asm_name)}')
			assert block.read(2) == b'\x04\x01'
			print(f'Model: {to_str(block.read_str())}')
			assert block.read1() == 0x01, block.xxd()
			block.read(1)
			assert block.read1() == 0x01, block.xxd()

			mem_model = block.read1()
			if   mem_model == 0x01:
				mem_model_str = 'SMALL'
			elif mem_model == 0x04:
				mem_model_str = 'LARGE'
			else: assert False, block.xxd()
			print(f'Memory model: {mem_model_str}')

			assert block.read(2) == b'\x03\x01', block.xxd()
			block.skip_zero(1)
			block.read(3)
			block.skip_zero(2)

		elif block_type == 0x80:
			# this block contains info about ROM window etc.
			block.read()
			pass

		elif block_type == 0x20:
			assert asm_name == block.read_str()
			assert block.read(1) == b'\x02', block.xxd()
			block.skip_zero(4)

		elif block_type == 0xe:
			# fn id, size and name
			# (name is prefixed with '$$' for some reason)
			print('Objects with constant storage')

			# everything with storage in .OBJ
			while block.readable():
				block.skip_zero(1)
				_id = block.read_int()
				_type = block.read1()

				# TODO what is this used for?
				block.read1()

				misc_1 = block.read(0x04) # block[0x05:0x09]
				block.skip_zero(0x03)
				_access = block.read1()
				misc_2 = block.read(0x02)
				block.skip_zero(0x03)

				obj_size = block.read_int()
				block.skip_zero(2)
				misc_3 = block.read1() # offset 0x16
				block.skip_zero(2)

				_name = to_str(block.read_str())

				if _name == '': # no name??? related to `main`
					assert misc_1 == b'\x00\x02\x00\x02'
					assert misc_2 == b'\x00\x02'
					assert misc_3 == 0x00
				elif _name == '$STACK':
					# Preallocated memory for stack. Its size
					# == allocated stack size.
					assert misc_1 == b'\x04\x00\x00\x00', (\
						_name, misc_1, block.xxd())
					assert misc_2 == b'\x00\x00'
					assert misc_3 == 0x01
				else:
					assert misc_1 == b'\x00\x00\x00\x00', (\
						_name, misc_1, block.xxd())
					assert misc_2 == b'\x00\x00'
					assert misc_3 == 0x01

				obj_data[_id] = bytearray(b'\x00') * obj_size
				print(f'  {get_type(_type)} {access_spec(_access)}'+
					f'  {_name}, #{_id}, {obj_size}B')

		elif block_type == 0x17:
			print('Global variables')
			while block.readable():
				block.skip_zero(1)
				var_id = block.read_int()
				assert block.read(1) == b'\x01'
				block.skip_zero(2)
				_access = block.read1()
				block.skip_zero(5)
				var_adr = block.read_int()
				block.skip_zero(2)
				_name = to_str(block.read_str())

				assert var_id not in nameof_defvar
				nameof_defvar[var_id] = _name

				print(f'  {access_spec(_access)} '+
					f'{_name}, #{var_id} @{var_adr}')

		elif block_type == 0x16:
			# info about symbol name <-> id
			# (symbol name) = '_' + (function name)
			while block.readable():
				block.skip_zero(1)
				_id = block.read_int()
				_type = block.read1()
				block.skip_zero(0x03)

				_access = block.read1()

				block.skip_zero(0x01)
				block.read1() # TODO 0x2e if _vsprintf_nn, else 0
				block.read1() # TODO 0x01 if __Ctype, else 0
				block.skip_zero(0x02)
				_name = block.read_str()

				nameof_export[_id] = to_str(_name)
				typeof_export[_id] = \
					f'{get_type(_type)} {access_spec(_access)}'
				print(typeof_export[_id] +
					f' {to_str(_name)}, #{_id}')

		elif block_type == 0x18:
			print('Dcl fn/extern var:')
			while block.readable():
				block.skip_zero(1)
				_id = block.read_int()
				_type = block.read1()
				_access = block.read1()
				block.skip_zero(1)
				_name = block.read_str()

				nameof_dcl[_id] = to_str(_name)
				print(f'  {get_type(_type)} {access_spec(_access)}'+
					f' {to_str(_name)}, #{_id}')


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
				0x80,  # weird thing related to `main`
			), (obj_type, block.xxd())
			read_data = block.read()

			# AFAIK, Rasu8 order the blocks correctly
			obj_data[obj_id] \
				[start_address:start_address+len(read_data)] \
				= read_data
			# however not all parts must be initialized ...

			last_block6_id = obj_id
			print(f'Block 6 for #{obj_id}, start {start_address}, len {len(read_data)}')
			# TODO fun thing about the object named '' is that
			# this returns out of range

		elif block_type == 0x08:
			'''
			Contains info about functions or global/extern
			variables used in the function in the 0x06 block
			right before this block.
			'''

			# currently this can't parse all types correctly.
			if not parse_0x08: continue

			print('External addresses for fn ' +
				nameof_export.get(last_block6_id, '<unnamed>'))
			# unnamed: something related to `_main`

			while block.readable():
				call_adr = block.read_int() # offset 0
				is_struct = block.read1()

				# 0x07: bitfield, 0x00: not
				is_bitfield = block.read1()
				block.skip_zero(1)

				'''
				0x01: far fn call
				0x0c: dsr get for var
				0x00: address get for var (for both NEAR and FAR)
				'''
				cmd_type = block.read1()

				# 1: deffn, 2: dclfn/extern, 3: var
				_type2 = block.read1() # offset 6

				_id = block.read_int() # offset 7

				_access = block.read1()

				block.skip_zero(1)
				offset = block.read_int() # offset 0b
				block.skip_zero(2)

				_type = block.read1() # offset 0f

				name_dict = {
					1: nameof_export, 2: nameof_dcl, 3: nameof_defvar
				}[_type2]

				typestr = get_type(_type)
				typestr += ' ' + access_spec(_access)

				if   is_bitfield == 0x07:
					typestr += ' bitfield'
				elif is_bitfield == 0x00:
					pass
				else: assert False, is_bitfield

				if   is_struct == 0x01:
					typestr += ' struct'
				elif is_struct == 0x00:
					pass
				else: assert False, is_struct

				if   cmd_type == 0x01:
					assert get_type(_type) == 'fn', get_type(_type)
				elif cmd_type == 0x0c:
					typestr += ' (dsr)'
					assert get_type(_type) in ('var', 'const')
				elif cmd_type == 0x00:
					typestr += ' (adr)'
					assert get_type(_type) in ('var', 'const')
				elif cmd_type == 0x0b:
					# TODO found in the function named '' in main
					typestr += ' (0x0b???)'
				elif cmd_type == 0x0d:
					# TODO found in setbit or something, iirc
					typestr += ' (0x0b???)'
				else: assert False, cmd_type


				print(f'  {typestr}  ' +
					f'{name_dict[_id]}, call@{call_adr} Δ={offset}')

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
			block.xxd()
			block.read()
			print('')

		assert not block.readable(), block.xxd()

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
		parse_data(obj_file.read(), parse_0x08=True)

if __name__ == '__main__':
	main()
