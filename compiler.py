#!/usr/bin/python3
import re
import sys
import os

from lib_570esp import *

'''
Only provide 0 or 1 cmdline argument: output format.
'''
assert len(sys.argv) < 3, 'Too many command-line arguments'
output_format = 'k' if len(sys.argv) == 1 else dict(
	h = 'h', hex = 'h', hexadecimal = 'h',
	k = 'k', key = 'k', keys = 'k', keypresses = 'k',
	j = 'j', justcode = 'j', code = 'j', raw = 'j',
	l = 'l', loader = 'l',
	ll='ll', loader2='ll',
	llh='llh', loader2_hex='llh',
)[sys.argv[1]]

def canonicalize(st):
	''' Make (st) canonical. '''
	if '$' in st:
		st1, st2 = st.split('$', 1)
		return canonicalize(st1) + '$' + st2
	st = st.lower()
	st = st.strip()
	# remove spaces around non alphanumeric
	st = re.sub(r' *([^a-z0-9]) *', r'\1', st)
	return st

def del_inline_comment(line):
	return (line+'#')[:line.find('#')].rstrip()

def get_commands(filename):
	commands = {}

	file = open(filename, 'r')
	data = file.read().split('\n')
	file.close()

	in_comment = False
	for line_index, line in enumerate(data):
		line = line.strip()

		# multi-line comments
		if line == '/*':
			in_comment = True
			continue
		if line == '*/':
			in_comment = False
			continue
		if in_comment:
			continue

		line = del_inline_comment(line)
		if not line: continue

		try:
			address, command = line.split('\t')
		except ValueError:
			raise Exception(f'Line {line_index} '
				'has an unexpected number of tab characters')

		command = canonicalize(command)

		tags = [] # process tags (leading `{...}`)
		while command and command[0] == '{':
			i = command.find('}')
			if i < 0:
				raise Exception(f'Line {line_index} '
					'has unmatched "{"');
			tags.append(command[1:i])
			command = command[i+1:]

		assert command, f'Line {line_index} has empty command'

		for disallowed_prefix in '0x', 'call', 'goto', 'adr_of':
			assert not command.startswith(disallowed_prefix), \
			f'Command ends with "{disallowed_prefix}" in line {line_index}'
		assert not command.endswith(':'), \
			f'Command ends with ":" in line {line_index}'
		assert ';' not in command, \
			f'Command contains ";" in line {line_index}'
		assert command not in commands, f'Command f{command} '\
			f'appears twice - second occurence on line {line_index}'

		commands[command] = (int(address, 16), tuple(tags))

	return commands
commands = get_commands('builtins')

program = sys.stdin.read().split('\n')[::-1]
program =[canonicalize(del_inline_comment(line))for line in program]
result = [] # list of ints in range 0..255

labels = {}
adr_of_cmds = [] # list of (source adr, offset, target label)

home = None

while program:
	line = program.pop()

	if not line: # empty line
		pass

	elif ';' in line:
		''' Compound statement. Syntax:
		`<statement1> ; <statement2> ; ...`
		'''
		program.extend(reversed(line.split(';')))

	elif line[-1] == ':':
		''' Syntax: `<label>:`
		Special: If the label is 'home', it specifies the point to
		start program execution. By default it's at the begin.
		'''
		label = line[:-1]
		assert label not in labels, f'Duplicated label: {label}'
		labels[label] = len(result)

	elif line.startswith('0x'):
		''' Syntax: `0x<hexadecimal digits>` '''
		assert len(line)%2==0, f'Invalid data length: {line}'
		n_byte = len(line)//2-1
		data = int(line, 16)
		for _ in range(n_byte):
			result.append(data&0xFF)
			data>>=8

	elif line.startswith('call'):
		''' Syntax: `call <address>` or `call <built-in>`. '''
		try:
			adr = int(line[4:], 16)
		except ValueError:
			adr = commands[line[4:].strip()][0]

		assert 0 <= adr < 0x20000, f'Invalid address: {line}'
		adr = optimize_adr_for_npress(adr)
		program.append(f'0x{adr+0x30300000:0{8}x}')

	elif line.startswith('goto'):
		''' Syntax: `goto <label>` '''
		label = line[4:]
		program.extend((
			'call sp=er14,pop er14',
			f'er14 = adr_of [-2] {label}'
		))

	elif line.startswith('adr_of'):
		''' Syntax: `adr_of [offset] <label>` | `adr_of <label>` '''
		line = line[6:].strip()
		if line[0] == '[':
			i = line.index(']')
			offset = int(line[1:i])
			label = line[i+1:].strip()
		else:
			offset = 0
			label = line.strip()

		adr_of_cmds.append((len(result), offset, label))
		result.extend((0,0))

	elif line in commands:
		''' `<built-in>`. Equivalent to `call <built-in>`. '''
		program.append('call '+line)

	elif '=' in line:
		''' Syntax:
		`register = <value> [, adr_of <label> [, ...]]`
		'''
		i = line.index('=')
		register, value = line[:i], line[i+1:].lstrip()

		assert '=' not in value, f'Nested assignment in {line}'
		value = value.replace(',', ';')

		program.extend((value, f'call pop {register}'))

	elif line[0] == '$':
		''' Python eval. '''
		x = eval(line[1:])
		if isinstance(x, str):
			program.append(x)
		else:
			program.extend(x)

	elif line.startswith('org'):
		hx = eval(line[3:])
		home = hx - len(result)

	else:
		assert False, f'Unrecognized command: {line}, {program[-1:-5:-1]}'

adr_of_cmds = [(source_adr, labels[target_label]+offset)
    for source_adr, offset, target_label in adr_of_cmds]

if output_format in ('k', 'h'):
    assert len(result) <= 100, f'Program too long ({len(result)} bytes)'

# now it's a list of (source adr, offset relative to `home`)

if home == None:
    if output_format not in ('l', 'll', 'llh'):
        home = 0x8DA4 # initial value of SP before POP PC
        if home + len(result) > 0x8E00:
        	sys.stderr.write('Warning: Program longer than 92 bytes (%d bytes)\n'%len(result))
        if 'home' in labels: home -= labels['home'] # confusing? ...
    
        min_home = home
        while min_home >= 0x8154+200: min_home -= 100
        while home + len(result) <= 0x8E00: home += 100 # 0x8E00: end of RAM
        home = min(range(min_home, home, 100), key=lambda home:
        	(
        		sum( # count number of ... satisfy condition
        			get_npress_adr(home+home_offset) >= 100
        			for source_adr, home_offset in adr_of_cmds),
        		-home # if ties then take max `home`
        	)
        )
    elif output_format in ('ll', 'llh'):
        home = 0x85ba
        if (home + labels.get('home', 0) - 2) % 256 == 0:
            home += 1
        assert home + len(result) <= 0x8e00, "Program too long"
    else:
        home = 0x85b0 - len(result)
        entry = home + labels.get('home', 0) - 2
        result.extend((0x6a, 0x4f, 0, 0, entry & 255, entry >> 8, 0x68, 0x4f, 0, 0))
        while home + len(result) < 0x85d7:
            result.append(0)
        result.extend((0xff, 0xae, 0x85))
        home2 = 0
        assert (home - home2) >= 0x8501, 'Program too long (%d bytes overflow)'%(0x8501-home+home2)
        while get_npress_adr(home - home2) >= 100:
            home2 += 1

# home is picked now, now substitute in the result
for source_adr, home_offset in adr_of_cmds:
    target_adr = home + home_offset
    assert result[source_adr] == 0
    result[source_adr] = target_adr & 0xFF
    assert result[source_adr+1] == 0
    result[source_adr+1] = target_adr >> 8

# scroll it around (use the most inefficient way)
hackstring = list(map(ord,'1234567890'*10)) # but still O(n)
for home_offset, byte in enumerate(result):
	assert isinstance(byte, int), (home_offset, byte)
	hackstring[(home+home_offset-0x8154)%100] = byte

for i, j in labels.items():
    print(i, '=', hex(home + j))

# done
if output_format == 'h':
	print(''.join(f'{byte:0{2}x}' for byte in hackstring))
elif output_format == 'j':
	print('0x%04x:'%home, *map('%02x'.__mod__, result))
elif output_format == 'l':
	print('%s %s:'%(to_key((home - home2) & 255), to_key((home - home2) >> 8)))
	for i in range(home2):
            result.insert(0, 0)
	import keypairs
	print(keypairs.format(result))
elif output_format == 'll':
	import keypairs
	print('%s %s:'%(keypairs.get_pair((home + len(result) - 1) & 255), keypairs.get_pair((home + len(result) - 1) >> 8)))
	entry = home + labels.get('home', 0) - 2
	if home != 0x85ba: result.insert(0, 0)
	result[:0] = (0x30, 0x6a, 0x4f, 0x30, 0x30, entry & 255, entry >> 8, 0x68, 0x4f, 0x30, 0)
	result.reverse()
	print(keypairs.format(result))
elif output_format == 'llh':
	print(bytes(result).hex())
else:
	assert output_format == 'k', 'Internal error'
	print(' '.join(map(to_key, hackstring)))
