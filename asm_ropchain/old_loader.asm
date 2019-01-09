start:
	getkeycode
	er8 = er0
	getkeycode
	r2 = r0
	r0 = r8, pop r8
	0x3333 # not important, for r8
	set lr
	er0 += er2
	r2 = r0    # now r2 holds the bytevalue

	# store that bytevalue to (*y)
	pop er0
y: # address to write to
	0xf830
	[er0] = r2

	# increment (y)
	er2 = 0x0101
	call 0x1852c # those 3 lines set er2 to 1
	er8 = adr_of [-200] y
	[er8] += er2, pop xr8
	0x33333333 # not important

	# restore the stack
	xr0 = adr_of [-117] start, adr_of [-217] start
	strcpy_null

home:
	goto start
