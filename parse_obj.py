#!/usr/bin/python3

'''
(Attempt to) parse an `.obj` file.

Because I'm not 100% sure about the file format (and 100% of what I
know is obtained by guessing, something may be wrong.

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

def parse_data(data):
	data = BytesIO_(data)
	sizeof_fn_id = {}
	while data.readable():
		block_type = data.read(1)[0]
		block_size = data.read_int()
		block = data.read(block_size)

		print(f'Block: type {hex(block_type)}, size '
			+f'{hex(block_size)}, sum {hex(sum(block))}')

		block_checksum = block[-1]
		block = BytesIO_(block[:-1])

		if block_type == 0x2:
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
			while block.readable():
				block.skip_zero(1)
				fn_id = block.read_int()
				block.skip_zero(0x0f)
				assert fn_id not in sizeof_fn_id
				sizeof_fn_id[fn_id] = block.read_int()
				assert block.read(0x05) == b'\x00\x00\x01\x00\x00'
				fn_name = block.read_str()
				print(f'Fn {to_str(fn_name)}, id {fn_id}, '+
					f'size {sizeof_fn_id[fn_id]}')

		elif block_type == 0x16: 
			# info about symbol name <-> id
			# (symbol name) = '_' + (function name)
			while block.readable():
				block.skip_zero(1)
				fn_id = block.read_int()
				block.skip_zero(0x0a)
				fn_name = block.read_str()
				print(f'Fn {to_str(fn_name)}, id {fn_id}')

		elif block_type == 0x18:
			assert block.read(2) == b'\x00\x01'
			block.skip_zero(4)
			assert to_str(block.read_str()) == '_main'

		elif block_type == 0x06:
			# function code
			block.skip_zero(5)
			fn_id = block.read_int()
			block.skip_zero(1)
			fn_code = block.read()
			assert len(fn_code) == sizeof_fn_id[fn_id]

		elif block_type == 0x08:
			# contains info which functions a function calls
			call_adr = block.read_int()
			block.skip_zero(3)
			assert block.read(2) == b'\x01\x01'
			target_id = block.read_int()
			block.skip_zero(7)

		elif block_type == 0x13:
			print('Source file name(s):')
			assert block.read(1) == b'\x0a'
			n_file = block.read_int()
			for file_index in range(n_file):
				assert block.read_int() == file_index
				block.read(1) # unknown, checksum or something
				block.skip_zero(3)
				print(f'+ {to_str(block.read_str())}')

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
			print('Unknown block')
			xxd(block.getbuffer())
			block.read()
			print()

		assert not block.readable(), xxd(block.getbuffer())

# ==============

if len(sys.argv) != 2:
	raise Exception('Please provide 1 argument, path to an .obj file')

with open(sys.argv[1], 'rb') as obj_file:
	parse_data(obj_file.read())

