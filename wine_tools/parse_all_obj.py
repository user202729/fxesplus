#!/usr/bin/python3
FOLDER_PATH = 'obj/'
ROM_PATH = '../rom.bin'

import sys
sys.path.append('..')
from parse_obj import parse_data
import os

with open(ROM_PATH, 'rb') as rom_file:
	rom = rom_file.read()

a = set()

for file in os.listdir(os.fsencode(FOLDER_PATH)):
	filename = os.fsdecode(file)
	with open(FOLDER_PATH + filename, 'rb') as obj_file:
		data = parse_data(obj_file.read(), print = lambda x:0)
	for obj_id, obj_name in data['nameof_export'].items():
		if data['typeof_export'][obj_id] != 'fn':
			continue
		fn_code = data["obj_data"][obj_id]
		fn_len = len(fn_code)

		print(f'Fn {obj_name}, len {fn_len}')

		for i in range(0, len(rom)-fn_len, 2):
			'''
			try matching 'rom[i:i+fn_len]' with fn_code.
			the algorithm used here is not 100% accurate (it should
			only match if the 00-00 comes after a L/ST/SB/TB/RB/
			LEA/B/BL) (see 'out.asm' for more details)
			but hopefully it's accurate enough

			This is not the most efficient possible algorithm but
			it runs fast enough (48.5s on my machine).
			'''
			for j in range(0, fn_len, 2):
				if not (
					rom[i+j:i+j+2] == fn_code[j:j+2] or
					fn_code[j:j+2]  == b'\x00\x00'   or
					(
						j+2 != fn_len                  and
						fn_code[j+2:j+4] == b'\x00\x00' and
						rom[i+j] == fn_code[j]          and
						(rom[i+j+1]^fn_code[j+1])&0xf0 == 0
					)
				): break
			else: # cannot found any mismatch
				print(f'ROM address {hex(i)[2:]}')

