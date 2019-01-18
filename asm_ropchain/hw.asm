data: 
	0x303132333435

home:
	r0 = r2 = 0
	er0 = use_buffer
	[er0] = r2

	xr0 = 0x01, 0x01, adr_of data
	line_print

	getkeycode
