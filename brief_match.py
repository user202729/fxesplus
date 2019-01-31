#!/bin/python3
'''
NOTE:
	The implementation in this branch is not very carefully tested.

Find a snippet of code in another file, using "disassembly brief form".

To create input files: disassemble using disas/nX-U8_brief.txt.
To use: ./brief_match.py <snippet> <file>

Currently use a relatively slow algorithm, and Python is also slow.
KMP or suffix tree may be used to speed up.

Function find_sublist and the while loop to find maximum `end` value
may be configured to accept a few errors.
'''

last_num=0
line_to_num={}

def read_file(filename):
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

def find_sublist(a,b):
	for i in range(len(b)-len(a)+1):
		if all(a[j]==b[i+j] for j in range(len(a))):
			return i
	return -1

def process(l1num,l1,l2num,l2):
	result=[]  # list of (line index 1, number of lines, line index 2)
	last_end=0
	for i in range(len(l1)):
		end=max(last_end,i)
		while end!=len(l1):
			index=find_sublist(l1[i:end+1],l2)
			if index<0:
				break
			good_index=index
			while end!=len(l1) and l1[end]==l2[index-i+end]:
				end+=1
		if end>last_end:
			last_end=end
			if find_sublist(l1[i:end],l2[good_index+1:])<0:
				# unique appearance
				result.append((i,end-i,good_index))
	return result

def main():
	import sys
	if len(sys.argv)!=3:
		print('Wrong number of arguments')
		sys.exit()

	l1num,l1=read_file(sys.argv[1])
	l2num,l2=read_file(sys.argv[2])

	for i,length,j in process(l1num,l1,l2num,l2):
		print(f'[{l1num[i]} .. {l1num[i+length]}] --> [{l2num[j]} ..]')

if __name__ == "__main__":
	main()
