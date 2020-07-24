# Tested

	0x01fe # er14: calc_checksum n-byte count. must be even (otherwise loop forever)

home:
	org 0xd544 # mode 100 + 10

	call calc_checksum_2
		0x303030303030 # qr8 rest
		adr_of y # er14
	call pr_checksum_2

	0x34333231 # excess/pad. max 4 bytes. The printed line will start from this
	0x36353433323130393837363534333231 # er14 buffer. store_reg_to_stack will write to this region
	# SP will always with restored to the correct position when the function returns

y:
	0x3030303030303030 # qr8

	0xd52c # er0 = dest : undo buf + 0xa
	0xd252 # er2 = src : cache + 0xa = delta (mod 4 == 2)
	0x30303030 # qr0 rest


	call smart_strcpy_nn_ # keep er2 unchanged, xr8 er12 changes
	# after this lr is good

	call pop qr8, pop qr0
	adr_of [-0x2da] start_value # er8: dif between cache and undo
	0x30303030 # r10~13, unused
	adr_of [-2] home # er14
	0x3231 #er0, unused
	0x3432 #er2 (must be ==2 mod 4)
	0x38373635 #r4~ 7

	nop

	call r0=0, [er8] += er2, pop xr8 # only modify er2, lr and er14 unchanged

	0x3030 # er8: initial subtract value (calc checksum)
start_value: # must be odd (so LSB != nul, so strcpy can work properly)
	0x3131 # er10

	# == goto home
	call mov sp, er14, pop er14
