# let y = home - 242, z = home - 252

home:
	# num y = 1
	xr0 = adr_of [-242] home, 0x01, 0x30
	num_fromdigit

	# num z = 1
	er0 = adr_of [-252] home
	num_fromdigit

	r0 = r2 = 0
	er0 = use_buffer
	[er0] = r2

loop:
	# y += z
	xr0 = adr_of [-242] home, adr_of [-252] home
	num_add

	er0 = adr_of [-242] home
	num_output_print

	# set lr
	# render

	set lr
	er0 = 0x03e8
	delay

	# restore the stack
	xr0 = adr_of [-132] home, adr_of [-232] home
	strcpy_null

	goto loop
