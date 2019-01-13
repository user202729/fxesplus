loop:
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
	0xb3b3 # ( Ans
after_y:
	[er0] = r2

	# decrement (y)
	er2 = 0xffff
#	call 0x1852c # those 3 lines set er2 to 1
	er8 = adr_of y
	[er8] += er2, pop xr8
	strcpy

	# restore the stack
	xr0 = adr_of loop, adr_of loop_bak
	er12 = 0x8df0
	strcpy
	goto loop
loop_bak:
	getkeycode
	er8 = er0
	getkeycode
	$[result.pop(), result.append(0), []][2]
the_end:
