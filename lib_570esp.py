def get_font(filename = 'font'):
	file = open(filename, 'r')
	font = ''

	for line_index, line in enumerate(file):
		if line_index == 16:
			break

		if line[-1] == '\n':
			line = line[:-1]

		if len(line) > 16:
			raise Exception(f'Line {line_index} in font \
file {filename} has more than 16 chars: "{line}"')
		font += line.ljust(16)

	file.close()
	if line_index != 16:
		raise Exception(f'Font file {filename} has less \
than 16 lines')

	return font
font = get_font()

font_assoc = dict((c,i) for i,c in enumerate(font))
def from_font(st):
	return [font_assoc[char] for char in st]
def to_font(charcodes):
	return ''.join(font[charcode] for charcode in charcodes)

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

consts = list(range(1,16))
for i in range(25):
	consts.append(rom[0x160E + i])
convs = list(range(0xD7, 0xFF))

def to_keys(charcodes):
	''' Returns a list of strings. '''
	keys = []
	for i in charcodes:
		try:
			keys.append(f'cs{1+consts.index(i)}')
			continue
		except ValueError:
			pass

		try:
			keys.append(f'cv{1+convs.index(i)}')
			continue
		except ValueError:
			pass

		keys.append(symbols[i])

	return keys

