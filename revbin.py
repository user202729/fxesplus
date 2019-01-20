#!/bin/python
'''
Reverse raw binary dump.
'''

import sys
data = ''.join(x for x in sys.stdin.read() if x in '01')
assert len(data)%8==0
sys.stdout.buffer.write(int(data,2).to_bytes(len(data)//8,'big'))
