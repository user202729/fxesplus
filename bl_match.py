#!/usr/bin/python
'''
Match the common prefix of 2 files, find BL addresses.

Useful when trying to determine the calculator ROM from small segments,
i.e., when dumping the ROM.

Note: this program doesn't find the matching address automatically.
brief_match.py must be used.

Example usage:

	../bl_match.py 82espa_3010.bin <(tail -c+$((0x2f94+1)) ../rom.bin )

'''

import sys
if len(sys.argv)!=3:
	print('Wrong number of arguments')
	sys.exit()

with open(sys.argv[1],'rb') as f: d1=f.read()
with open(sys.argv[2],'rb') as f: d2=f.read()

nbyte=min(len(d1),len(d2))

print(f'Similarity ratio: {sum(map(int.__eq__,d1,d2))/nbyte*100}%')

for i in range(0,nbyte-2,2):
	if d1[i]==d2[i]==0x01 and d1[i+1]&0xf0==0xf0 and d2[i+1]&0xf0==0xf0:
		print(' {:06X} - {:06X}'.format(
			(d1[i+1]&0xf)<<16|d1[i+3]<<8|d1[i+2],
			(d2[i+1]&0xf)<<16|d2[i+3]<<8|d2[i+2]
			))
