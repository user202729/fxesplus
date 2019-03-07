#!/bin/python3

'''
Generate a random valid RAM for fx-ES PLUS calculators (such that the calculator won't
reset when it's boot).

Write output to file `ram.bin`.
'''

from random import randint
ram=bytearray(0xe00)

for i in range(len(ram)):
	ram[i]=randint(0,255)

ram[0x0dc]=randint(0,7)
ram[0x112]=randint(4,29)  # contrast
for i in range(0x226,0x226+10*10,10):  # variables
	ram[i]=randint(0,15)<<4|randint(0,9)
	ram[i+9]=randint(0,15)
ram[0x60e:0x60e+15]=range(0x0f,0x00,-1)  # magic string

with open('ram.bin','wb') as f:f.write(ram)
# import os
# os.system('./emu.sh ram=82espa/ram.bin preserve_ram=1')
