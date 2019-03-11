#!/bin/python3
'''
NOTE:
	Checkout branch `faster-briefmatch` for a faster implementation, and an
	implementation in C++.
	However that is not very carefully tested.

Find a snippet of code in another file, using "disassembly brief form".

To create input files: disassemble using disas/nX-U8_brief.txt.
To use: ./brief_match.py <snippet> <file>

Currently use a relatively slow algorithm, and Python is also slow.
KMP or suffix tree may be used to speed up.

Function find_sublist may be configured to accept a few errors.
'''

import sys
if len(sys.argv)!=3:
	print('Wrong number of arguments')
	sys.exit()

last_num=0
line_to_num={}

def process(filename):
	'''Read disassembly commands and address from filename.'''
	global last_num,line_to_num
	commands=[]
	linenums=[]
	with open(filename,'r') as f:
		for x in f.read().splitlines():
			linenums.append(x[:6])
			x=x[28:]
			try:
				commands.append(line_to_num[x])
			except KeyError:
				last_num+=1
				line_to_num[x]=last_num
				commands.append(last_num)
	return linenums,commands

l1num,l1=process(sys.argv[1])
l2num,l2=process(sys.argv[2])

def find_sublist(a,b):
	for i in range(len(b)-len(a)+1):
		if all(a[j]==b[i+j] for j in range(len(a))):
			return i
	return -1

last_end=0
for i in range(len(l1)):
	end=max(last_end,i)
	while end!=len(l1) and find_sublist(l1[i:end+1],l2)>=0:
		end+=1
	assert end>=last_end
	if end>last_end:
		last_end=end
		print(f'[{l1num[i]} .. {l1num[end-1]}] --> [{l2num[find_sublist(l1[i:end],l2)]} ..]')
