# Invoking this directly does nothing, instead, import this as a library.

def get_font(filename = 'font'):
	file = open(filename, 'r')
	font = ''

	for line_index, line in enumerate(file):
		if line_index == 16:
			break

		if line[-1] == '\n':
			line = line[:-1]

		if len(line) > 16:
			raise Exception(f'Line {line_index} in font file '+
				f'{filename} has more than 16 chars: "{line}"')
		font += line.ljust(16)

	file.close()
	if line_index != 16:
		raise Exception(f'Font file {filename} has less than '+
			'16 lines')

	return font
font = get_font()

font_assoc = dict((c,i) for i,c in enumerate(font))
def from_font(st):
	return [font_assoc[char] for char in st]
def to_font(charcodes):
	return ''.join(font[charcode] for charcode in charcodes)

def get_npress(charcodes):
	npress=(
	999,4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
	100,100,100,100,100,100,100,100,100,100,100,100,100,4,  4,  4,
	100,100,4,  4,  4,  2,  4,  4,  1,  1,  4,  1,  1,  1,  1,  100,
	1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  4,  100,2,  100,100,
	4,  2,  2,  2,  2,  2,  2,  100,100,100,100,100,100,100,1,  1,
	100,100,100,100,2,  100,100,2,  2,  2,  100,100,1,  100,1,  100,
	1,  100,100,2,  100,100,100,100,1,  2,  1,  2,  2,  2,  100,100,
	2,  2,  2,  2,  1,  1,  2,  1,  4,  4,  4,  100,100,100,100,100,
	100,2,  2,  100,100,3,  3,  3,  100,100,100,1,  2,  100,100,100,
	2,  2,  2,  2,  100,100,100,100,1,  100,100,100,100,100,100,2,
	1,  1,  1,  1,  100,100,100,100,2,  100,100,100,100,100,1,  100,
	2,  2,  2,  2,  4,  4,  4,  4,  100,100,100,100,100,100,2,  2,
	100,100,2,  100,4,  4,  4,  4,  100,100,100,100,100,100,100,100,
	100,100,100,100,4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
	4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
	4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  100,
	)
	if isinstance(charcodes, int): charcodes = (charcodes,)
	return sum(npress[charcode] for charcode in charcodes)

def get_npress_adr(adrs):
	if isinstance(adrs, int): adrs = (adrs,)
	assert all(0 <= adr < 0x20000 for adr in adrs)
	return sum(get_npress((adr&0xFF,(adr>>8)&0xFF)) for adr in adrs)

def optimize_adr_for_npress(adr):
	'''
	For a 'POP PC' command, the lowest significant bit in the address
	does not matter. This function use that fact to minimize number
	of key strokes used to enter the hackstring.
	'''
	return min((adr, adr^1), key=get_npress_adr)

def get_binary(filename):
	file = open(filename, 'rb')
	result = file.read()
	file.close()
	return result
rom = get_binary('/home/user202729/fxesplus/rom.bin')

def get_symbols(rom):
	symbols = [''] * 256
	for i in range(1, 256):
		ptr_adr = 0x10F2 + 2*i
		ptr = rom[ptr_adr+1] << 8 | rom[ptr_adr]

		info = rom[0x12F2 + i]
		symbol_len = info & 0xF
		symbol_type = info >> 4 # if 15 then func else normal

		if symbol_type != 15: ptr += symbol_type

		result = to_font(rom[ptr:ptr+symbol_len])
		if symbol_type == 15: result = result + '('
		symbols[i] = result

	return symbols
symbols = get_symbols(rom)

consts = [*range(1,16)] + [rom[0x160E + i] for i in range(25)]
convs = [*range(0xD7, 0xFF)]

def to_key(byte):
	try:
		return f'cs{1+consts.index(byte)}'
	except ValueError:
		pass

	try:
		return f'cv{1+convs.index(byte)}'
	except ValueError:
		pass

	return symbols[byte]

def optimize_sum_for_npress(total):
	''' Return (a, b) such that a + b == total. '''
	return ['0x'+hex(x)[2:].zfill(4) for x in min(
		((x, (total-x)%0x10000) for x in range(0x0101, 0x10000)),
		key=get_npress_adr
	)]
