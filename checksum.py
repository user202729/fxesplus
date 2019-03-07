#!/bin/python3
with open('rom.bin','rb') as f:
	d=f.read()
	assert len(d)==0x20000
	cs=(-sum(d[:-4]))%0x10000
	c1=int.from_bytes(d[-4:-2],'little')  # expected checksum value
	print(hex(cs),'==' if cs==c1 else '!=',hex(c1))
