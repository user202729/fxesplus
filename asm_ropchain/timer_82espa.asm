# let y = 0x8142, z = 0x1b9e
# note that on program start, y==0 and z==1

home:
	r0 = r2 = 0
	er0 = use_buffer
	[er0] = r2

loop:
	# y += z
	xr0 = 0x8142, 0x1b9e
	num_add

	er0 = 0x8142
	num_output_print

	# set lr
	# render

	set lr
	er0 = 0x03e8
	delay

	# restore the stack
	xr0 = adr_of [-220] home, adr_of [-320] home
	strcpy_null

	goto loop
