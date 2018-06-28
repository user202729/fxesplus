# f_24A3A refers a "char***" data structure. What's there inside it...
tables=0x6f04
max_nchar=17
n_entry=328

with open('rom-emu.bin','rb') as file:rom=file.read()

def from_256(digits):
	''' convert from base 256.
	Equivalent to interpret as little endian wide integer. '''
	return digits[0]|from_256(digits[1:])<<8 if digits else 0
def fetch_int(adr):
	''' 1 int = 2 bytes. little endian '''
	return from_256(rom[adr:adr+2])

for adr_table in range(tables,tables+2,2):
	table=fetch_int(adr_table)
	table_len=0
	for adr_string in range(table,table+2*n_entry,2):
		string=fetch_int(adr_string)
		str_len=rom[string:string+2*max_nchar].find(0)
		str_content=rom[string:string+str_len]
		nchar=sum(ch<0xf0 for ch in str_content)
		if nchar>max_nchar: # str_len<0
			break
		if table_len==0:
			print(f'* {table:#0{6}x}\n')
		table_len+=1
		print(f'    {string:0{4}x}\t'+
			repr(chr(rom[string-1])).ljust(8)+
			repr(rom[string:string+str_len])[1:])
	if table_len==0:break
	print()
