#!/bin/python
from collections import *
from sys import stdin
d=stdin.buffer.read()
cnt=Counter(d[i]|d[i+1]<<8 for i in range(0,len(d),2))
for x,freq in cnt.most_common(10):
	print(f'{x:04x}\t{freq}')
