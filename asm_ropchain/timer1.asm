# let y = home - 242, z = home - 252

home:
	# num y = 1
	xr0 = 0x8154, 0x01, 0x30
	num_fromdigit

	# num z = 1
	er0 = 0x8160
	num_fromdigit

	r0 = r2 = 0
	er0 = use_buffer
	[er0] = r2

loop:
	# y += z
	xr0 = 0x8154, 0x8160
	num_add

	er0 = 0x8154
	num_output_print

	# set lr
	# render

	set lr
	er0 = 0x03e8
	delay

	# restore the stack
	xr0 = 0x82C2, 0x825E
	strcpy_null

	goto loop
