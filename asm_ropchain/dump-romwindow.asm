y:
	# qr8
	0x3031323334353637
	# xr4
	0x33323130

home:

	pop er0
	0x3030
	delay

	pop er0
	0x1f; 0x30
	pop er2
	0xf810

	# render + 0x10
	call 0x313c

	# source position
	0x3232

	# qr8
	0x303132333435
	adr_of y

	# xr4
	0x38373635

	call 0x2fac
