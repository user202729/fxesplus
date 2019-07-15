# Get ROM of segment 0 - 580VNX.
# Set f004 to 1 each time. :(
# works on emu.

# compiled:

# 0xd542: <fe> <01> 4 cos⁻¹( 1 0 <01> <fe> <04> <f0> ⁻¹ ³√( 1 0 𝐏 𝐅 2 0 0 0 0 0 0
# 0 cosh⁻¹( ² 𝐞 𝐅 2 0 . . . . . . . . . . . . . . . . 0 0 0 0 0 0 0 0 , ² d/d𝒙(
# ▸a+b𝐢 0 0 0 0 ⌟ <03> 2 0 <0c> M 2 0 - ▸a+b𝐢 0 0 0 0 0 0 × × 0 0 or <9c> 0 0 0 0
# 1 <fe> <12> ÷ 0 0 A ² × × 0 0 <10> ÷ 0 0

# special chars required: [f0   ^-1] [f] [f]  >a+bi <03> >a+bi or <9c>
# -> f0 d4 3f 3f d2 03 d2 a0 9c

# 2. f0 d4 d2 d2 a0 19 9c
# -> @49 f d d d a c
# [f0 d4] __ [__ 3f] d2 [__ 03] d2 a0 19 9c
# [->] [__ 3f] [<-] x DEL [->] [->] [->] x DEL   AC

# RESULT: 5b65 -> e55c -> 4317 -> ....

t:
	0x01fe # er14: calc_checksum n-byte count. must be even
	# (on iterations != 0)

home:
	org 0xd544 # mode 100 + 10

	#xr0 = 0xf004, 0x01, 0x30
	#[er0] = r2

	xr0 = 0x01, 0xfe, 0xf004  # r1 can be arbitrary
	[er2] = r0, r2 = 0

	# now er4 = 0x01fe
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

	nop # to align z to good pos

	[er8] += er2, pop xr8 # only modify er2, lr unchanged

	0x3030 # er8: initial subtract value (calc checksum)
z:
	0xfe31 # er10: start address. should be odd (so LSB != nul)

	# == goto t:
	pop er14, rt
	adr_of t
	nop
	mov sp, er14, pop er14, rt


