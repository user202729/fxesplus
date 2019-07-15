# Get ROM of segment 0 - 580VNX.
# out: 80eb -> FREEZE

home:
	org 0xd544 # mode 100 + 10
	nop

	call calc_checksum_set_f004 # [f004] = 1, pop qr8 pc

	0x31;0x32;0x33;0x34;0x35;0x36
t:
	0x01fe # er14: calc_checksum n-byte count. must be even

	calc_checksum_0
		0x303030303030 # qr8 rest
		adr_of y # er14
	pr_checksum

	0x2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e # er14 buffer
	# 0x2e2e2e2e # excess. max 8 bytes

y:
	0x3030303030303030 # qr8

	0xd52c # er0 = dest : undo buf + 0xa
	0xd252 # er2 = src : cache + 0xa = delta (mod 4 == 2)
	0x30303030 # qr0 rest


	smart_strcpy_nn_ # keep er2 unchanged, xr8 er12 changes
	# after this lr is good

	pop qr8
	adr_of [-0x2da] z # dif between cache and undo
	0x303030303030

	# nop # to align z to good pos

	[er8] += er2, pop xr8 # only modify er2, lr unchanged

	0x3030 # er8: initial subtract value (calc checksum)
z:
	0xfe31 # er10: start address. should be odd (so LSB != nul)

	# == goto t:
	pop er14, rt
	adr_of t
	nop
	mov sp, er14, pop er14, rt


