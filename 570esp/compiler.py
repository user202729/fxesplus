#!/usr/bin/python3
import sys,os
os.chdir(os.path.dirname(__file__))
sys.path.append('..')
from libcompiler import (
		set_font, set_npress_array, get_disassembly, get_commands,
		read_rename_list, set_symbolrepr,
		to_font,
		process_program
		)

get_disassembly('disas.txt')
get_commands('gadgets')
read_rename_list('labels')
read_rename_list('../labels_sfr')


def get_font(filename = 'font'):
	file = open(filename, 'r', encoding='utf8')
	font = ''

	for line_index, line in enumerate(file):
		if line_index == 16:
			break

		if line[-1] == '\n':
			line = line[:-1]

		if len(line) > 16:
			raise Exception(f'Line {line_index} in font file '+
				f'{filename} has more than 16 chars: "{line}"')
		font += line.ljust(16)

	file.close()
	if line_index != 16:
		raise Exception(f'Font file {filename} has less than '+
			'16 lines')

	return font
set_font(get_font())

npress=(
	999,4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
	100,100,100,100,100,100,100,100,100,100,100,100,100,4,  4,  4,
	100,100,4,  4,  4,  2,  4,  4,  1,  1,  4,  1,  1,  1,  1,  100,
	1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  4,  100,2,  100,100,
	4,  2,  2,  2,  2,  2,  2,  100,100,100,100,100,100,100,1,  1,
	100,100,100,100,2,  100,100,2,  2,  2,  100,100,1,  100,1,  100,
	1,  100,100,2,  100,100,100,100,1,  2,  1,  2,  2,  2,  100,100,
	2,  2,  2,  2,  1,  1,  2,  1,  4,  4,  4,  100,100,100,100,100,
	100,2,  2,  100,100,3,  3,  3,  100,100,100,1,  2,  100,100,100,
	2,  2,  2,  2,  100,100,100,100,1,  100,100,100,100,100,100,2,
	1,  1,  1,  1,  100,100,100,100,2,  100,100,100,100,100,1,  100,
	2,  2,  2,  2,  4,  4,  4,  4,  100,100,100,100,100,100,2,  2,
	100,100,2,  100,4,  4,  4,  4,  100,100,100,100,100,100,100,100,
	100,100,100,100,4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
	4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
	4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  100,
	)
set_npress_array(npress)

def get_binary(filename):
	file = open(filename, 'rb')
	result = file.read()
	file.close()
	return result
rom = get_binary('rom.bin')

def get_symbols(rom):
	symbols = [''] * 256
	for i in range(1, 256):
		ptr_adr = 0x10F2 + 2*i
		ptr = rom[ptr_adr+1] << 8 | rom[ptr_adr]

		info = rom[0x12F2 + i]
		symbol_len = info & 0xF
		symbol_type = info >> 4 # if 15 then func else normal

		if symbol_type != 15: ptr += symbol_type

		result = to_font(rom[ptr:ptr+symbol_len])
		if symbol_type == 15: result = result + '('
		symbols[i] = result

	return symbols
symbols = get_symbols(rom)
symbolrepr = symbols[:]

consts = [*range(1,16)] + [rom[0x160E + i] for i in range(25)]
for i,x in enumerate(consts):
	symbolrepr[x]='cs'+str(i+1)
convs = [*range(0xD7, 0xFF)]
for i,x in enumerate(convs):
	symbolrepr[x]='cv'+str(i+1)

set_symbolrepr(symbolrepr)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', default='overflow',
			choices=('none', 'overflow', 'loader'),
			help='how will the output be used')
	parser.add_argument('-f', '--format', default='key',
			choices=('hex', 'key'),
			help='output format')
	args = parser.parse_args()

	program = sys.stdin.read().split('\n')

	process_program(args, program, overflow_initial_sp=0x8DA4)
