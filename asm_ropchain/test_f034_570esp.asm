 	er0 = 0x221d
 	print_4lines
 	set lr
x:
	er8 = 0xF034
	# er2 = 0x3001  # +30 <-> no-op for next byte (if nbit <= 4)
	er2 = 0x0101
	[er8] += er2, pop xr8
	0x34333231

	er0 = 0xf830
	[er0] = r2

	er0 = 0x2727
	delay
	goto x
