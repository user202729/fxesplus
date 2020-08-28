#!/usr/bin/python3
"""
Parses all .obj files in args.folder_path, match the function code against args.rom_path.
Prints all data, plus some debugging functions.
Grep for `Fn` for the found matchings.
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder-path', default='obj/',
		help='path to the folder containing .obj files')
parser.add_argument('-r', '--rom-path', default='../rom.bin',
		help='path to the rom to match against')
parser.add_argument('-v', '--verbose', action='store_true',
		help='path to the rom to match against')
args = parser.parse_args()

import sys
sys.path.append('..')
from parse_obj import parse_data
import os

with open(args.rom_path, 'rb') as rom_file:
	rom = rom_file.read()

a = set()

for filename in os.listdir(os.fsencode(args.folder_path)):
	filename = os.fsdecode(filename)
	with open(args.folder_path + filename, 'rb') as obj_file:
		data = parse_data(obj_file.read(), print = print if args.verbose else lambda *args, **kwargs: None)
	for obj_id, obj_name in data['nameof_export'].items():
		if 'fn' not in data['typeof_export'][obj_id]:
			continue
		fn_code = data["obj_data"][obj_id]
		fn_len = len(fn_code)

		if args.verbose:
			import xxd
			print("="*20, obj_name)
			xxd.xxd(fn_code)
			print("="*20)

		matches = []
		for i in range(0, len(rom)-fn_len, 2):
			'''
			Try matching 'rom[i:i+fn_len]' with fn_code.
			The algorithm used here is not 100% accurate (it should
			only match if the 00-00 comes after a L/ST/SB/TB/RB/
			LEA/B/BL) (see 'out.asm' for more details)
			but hopefully it's accurate enough.

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
				if matches:
					# multiple matches = bad
					matches = []
					break
				matches.append(i)

		if matches:
			print(f'Fn {obj_name}, adr {hex(matches[0])[2:]}')
