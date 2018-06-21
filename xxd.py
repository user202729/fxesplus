# xxd (default configuration) implemented in Python.
# Used as a library to import.

def xxd(data):
	hex_data = [hex(byte)[2:].zfill(2) for byte in data]
	ascii_data = [
		chr(byte) if 0x20<=byte<=0x7E else '.'
		for byte in data]

	# pad to multiple of 16
	rem = (-len(data))%16
	hex_data.extend(['  '] * rem)
	ascii_data.extend([' '] * rem)

	ascii_data = ''.join(ascii_data)

	for addr in range(0, len(hex_data), 16):
		print(hex(addr)[2:].zfill(4), end=': ')
		for i in range(0, 16, 2):
			print(''.join(hex_data[addr+i:addr+i+2]),end=' ')
		print('  '+ascii_data[addr:addr+16])
