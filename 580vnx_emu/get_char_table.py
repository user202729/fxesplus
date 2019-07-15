#!/bin/python
# reimplementation of f_208F2 - char to str

LOOKUP = {
		0x00:(0x247a,0x265a),
		#0xfa:(0x23a8,0x242a),
		#0xfe:(0x20da,0x22b8),
		#0xfd:(0x1fba,0x207a),
		#0xfb:(0x1eca,0x1f6a),
		}

with open(r'rom.bin','rb') as f:
	rom=f.read()

ROMWINDOW = 0xd000

def fetch(x):
	assert x%2 == 0
	return rom[x+1]<<8|rom[x]

def f(x):
	r0 = x & 0xff
	r1 = x >> 8
	if r0 == 0:
		return 0, ''

	try:
		er2, er4 = LOOKUP[r1]
	except KeyError:
		return 0, ''

	er2 = fetch(er2 + r0 * 2)  # address
	r0 = rom[er4 + r0]

	r4 = r0
	r0 &= 15
	if r0 == 0:
		return 0, ''
	r4 >>= 4
	r1 = r0  # length remaining
	if r4 != 15:
		er2 += r4

	result = bytearray()
	for r6 in range(1, 33):  # 33: max len
		r5 = rom[er2]
		assert er2 < ROMWINDOW
		result.append(r5)
		er2 = (er2 + 1) & 0xffff
		if r5 == 4 or r5 >= 0xf0:  # why 4? ...
			continue
		r1 -= 1
		if r1 == 0:
			break

	if r4 == 15:
		result += b'('
		r0 += 1

	return r0, bytes(result)  # r0: num of char (not byte), result: copied to input er2

if __name__=='__main__':
	for r1 in LOOKUP:
		for r0 in range(0x100):
			adr=r1<<8|r0
			nc,s=f(adr)
			print(hex(adr),nc,s)
			# no ram, unfortunately (?)
