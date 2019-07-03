#!/bin/python
'''
Reverse raw binary dump.
'''

import sys
data = ''.join(x for x in sys.stdin.read() if x in '01')
extra = len(data)%8
if extra:
	sys.stderr.write(f'Last {extra} bits truncated\n')
	data = data[:-extra]
if data:
	sys.stdout.buffer.write(int(data,2).to_bytes(len(data)//8,'big'))
