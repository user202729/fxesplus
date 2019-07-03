#!/bin/python3
"""
Convert output file of classwiz-get-font.lua to png file format.
Usage:
	Define suitable row, col, labels value.
	Set file path `../out` to correct file path.
	Run the program.
	Output is saved at a.png.
"""

from PIL import Image
import itertools
import numpy as np

with open('../out','r') as f:
	d=np.array([[int(y==' ') for y in line[:-1]] for line in f.readlines()])

row=17
col=11

labels=[ "  00:", "  10:", "  20:", "  30:", "  40:", "  50:", "  60:", "  70:", "  80:", "  90:", "  A0:", "  B0:", "  C0:", "  D0:", "  E0:", "F000:", "F010:", "F020:", "F030:", "F040:", "F050:", "F060:", "F070:", "F080:", "F090:", "F0A0:", "F0B0:", "F0C0:", "F0D0:", "F0E0:", "F100:", "F110:", "F120:", "F130:", "F140:", "F150:", "F160:", "F170:", "F180:", "F190:", "F1A0:", "F1B0:", "F1C0:", "F1D0:", "F1E0:", "F200:", "F210:", "F220:", "F230:", "F240:", "F250:", "F260:", "F270:", "F280:", "F290:", "F2A0:", "F2B0:", "F2C0:", "F2D0:", "F2E0:", "F300:", "F310:", "F320:", "F330:", "F340:", "F350:", "F360:", "F370:", "F380:", "F390:", "F3A0:", "F3B0:", "F3C0:", "F3D0:", "F3E0:", "F400:", "F410:", "F420:", "F430:", "F440:", "F450:", "F460:", "F470:", "F480:", "F490:", "F4A0:", "F4B0:", "F4C0:", "F4D0:", "F4E0:", "F500:", "F510:", "F520:", "F530:", "F540:", "F550:", "F560:", "F570:", "F580:", "F590:", "F5A0:", "F5B0:", "F5C0:", "F5D0:", "F5E0:", "F600:", "F610:", "F620:", "F630:", "F640:", "F650:", "F660:", "F670:", "F680:", "F690:", "F6A0:", "F6B0:", "F6C0:", "F6D0:", "F6E0:", "F700:", "F710:", "F720:", "F730:", "F740:", "F750:", "F760:", "F770:", "F780:", "F790:", "F7A0:", "F7B0:", "F7C0:", "F7D0:", "F7E0:", "F800:", "F810:", "F820:", "F830:", "F840:", "F850:", "F860:", "F870:", "F880:", "F890:", "F8A0:", "F8B0:", "F8C0:", "F8D0:", "F8E0:", "F900:", "F910:", "F920:", "F930:", "F940:", "F950:", "F960:", "F970:", "F980:", "F990:", "F9A0:", "F9B0:", "F9C0:", "F9D0:", "F9E0:", "FA00:", "FA10:", "FA20:", "FA30:", "FA40:", "FA50:", "FA60:", "FA70:", "FA80:", "FA90:", "FAA0:", "FAB0:", "FAC0:", "FAD0:", "FAE0:", "FB00:", "FB10:", "FB20:", "FB30:", "FB40:", "FB50:", "FB60:", "FB70:", "FB80:", "FB90:", "FBA0:", "FBB0:", "FBC0:", "FBD0:", "FBE0:", "FC00:", "FC10:", "FC20:", "FC30:", "FC40:", "FC50:", "FC60:", "FC70:", "FC80:", "FC90:", "FCA0:", "FCB0:", "FCC0:", "FCD0:", "FCE0:", "FD00:", "FD10:", "FD20:", "FD30:", "FD40:", "FD50:", "FD60:", "FD70:", "FD80:", "FD90:", "FDA0:", "FDB0:", "FDC0:", "FDD0:", "FDE0:", "FE00:", "FE10:", "FE20:", "FE30:", "FE40:", "FE50:", "FE60:", "FE70:", "FE80:", "FE90:", "FEA0:", "FEB0:", "FEC0:", "FED0:", "FEE0:", "FF00:", "FF10:", "FF20:", "FF30:", "FF40:", "FF50:", "FF60:", "FF70:", "FF80:", "FF90:", "FFA0:", "FFB0:", "FFC0:", "FFD0:", "FFE0:", ]

assert len(d)/row==len(labels)

def bl(r,c):
	return d[row*r:row*(r+1),col*c:col*(c+1)]

char={}
for c in '0123456789ABCDEF :':
	o=ord(c)
	char[c]=bl(o>>4,o&15)

d=np.concatenate(
		tuple(
			np.concatenate([*(char[c] for c in labels[r]),d[row*r:row*(r+1)]],axis=1)
			for r in range(len(labels))
			)
		)

im=Image.new('1',(len(d[0]),len(d)))
im.putdata(list(itertools.chain.from_iterable(d)))
im.save('a.png')
