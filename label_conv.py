#!/bin/python3
'''
Convert labels file for one ROM to another, using "disassembly brief form".

To create input files: disassemble using disas/nX-U8_brief.txt.
To use: ./label_conv.py [lab1] [dis1] [dis2]

Currently use `diff` utility to match brief disassembled files.
However, it appears that different calculator version use different registers.
'''

import re
import argparse
from sys import argv,exit,stderr
from subprocess import run
from tempfile import NamedTemporaryFile

parser=argparse.ArgumentParser()
parser.add_argument('lab1', nargs='?', default='570esp/labels',
		help='source labels file')
parser.add_argument('disn1', nargs='?', default='570esp/_b_disas.txt',
		help='source brief disassembly file')
parser.add_argument('disn2', nargs='?', default='82espa/_b_disas.txt',
		help='target brief disassembly file')
parser.add_argument('romwin', nargs='?', default=0x8000,
		type=lambda s:int(s,0),
		help='size of rom window')
args = parser.parse_args()


def adr(line):return int(line[:6],16)

with open(args.disn1,'r') as f: dis1=f.read().splitlines()
with open(args.disn2,'r') as f: dis2=f.read().splitlines()

codemap=[None]*(adr(dis1[-1])+1)

# note: fail if disn1/disn2 contains single quote
sedcmd="sed -E 's/.{28}//'"
for line in run(['bash','-c',
		f"diff <({sedcmd} '{args.disn1}') <({sedcmd} '{args.disn2}') "
		"--unchanged-group-format='%df %dl %dF %dL\n' --line-format="
		],capture_output=True).stdout.splitlines():
	f1,l1,f2,l2=[int(s)-1 for s in line.split()]
	assert l1-f1==l2-f2
	assert dis1[f1][28:]==dis2[f2][28:]
	nline=l1-f1+1
	if nline<5:continue

	f1=adr(dis1[f1]);l1=adr(dis1[l1])+1
	f2=adr(dis2[f2]);l2=adr(dis2[l2])+1
	# print(f'{f1:05X} .. {l1:05X} -> {f2:05X} .. {l2:05X} : {f2-f1: 5X} | nline = {nline}')
	codemap[f1:l1]=range(f2,l2)

datamap=[None]*0x10000
abs_adr_regex=re.compile(r'.{6} *[^ ]. .. ([^ ][^ ]) ([^ ][^ ])  [^\[]*')
ix2=0
for ix1,line in enumerate(dis1):
	codeadr1=adr(line)
	if codemap[codeadr1] is None: continue
	match=abs_adr_regex.fullmatch(line)
	if match and 'BL' not in line and (ix1==0 or 'DSR' not in dis1[ix1-1]):
		dataadr1=int(match[2]+match[1],16)
		codeadr2=codemap[adr(line)]
		while adr(dis2[ix2])!=codeadr2: ix2+=1
		# print(line)
		# print(dis2[ix2])
		match=abs_adr_regex.fullmatch(dis2[ix2])
		assert match
		dataadr2=int(match[2]+match[1],16)

		# print(f'{dataadr1:04X} -> {dataadr2:04X}')
		# if datamap[dataadr1] is not None and datamap[dataadr1]!=dataadr2:
			# print(f'{dataadr1:04X} -> {datamap[dataadr1]:04X}: conflict')
			# assert False
		datamap[dataadr1]=dataadr2

line_regex  =re.compile(r'^\s*([\w_.]+)')
global_regex=re.compile(r'f_([0-9a-fA-F]+)')
local_regex =re.compile(r'.l_([0-9a-fA-F]+)')
data_regex  =re.compile(r'd_([0-9a-fA-F]+)')
hexadecimal =re.compile(r'[0-9a-fA-F]+')

with open(args.lab1,'r') as f:
	for line in f.read().splitlines():
		match=line_regex.match(line)
		if not match:
			print(line)
			continue
		raw=match[1]
		if raw.startswith('.'):  # local labels are kept intact
			print(line)
			continue

		match=data_regex.fullmatch(raw)
		if match:
			raw=match[1]
			assert int(raw,16)<0x10000,raw
			addr=datamap[int(raw,16)]
			if addr is not None:
				print(f'd_{addr:0{len(raw)}X}'+line[len(raw)+2:])
			else:
				print(line+' # (???)')
			continue

		addr=None
		if hexadecimal.fullmatch(raw):
			addr=int(raw,16)
		else:
			match=global_regex.match(raw)
			if match:
				addr=int(match[1],16)
				if len(match[0]) != len(raw):
					match=local_regex.fullmatch(raw[len(match[0]):])
					if match:  # full address f_12345.l_67
						addr+=int(match[1],16)

		if addr is None:
			print(line)
			continue

		addr=codemap[addr]
		if addr is None:
			print('?'*len(raw)+line[len(raw):])
			continue

		print(f'{addr:0{len(raw)}X}'+line[len(raw):])
