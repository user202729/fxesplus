# 580VNX - Enter mode E2.

home:
	org 0xd544 # mode 100 + 10

	xr0 = 0xe2, 0x323130
	call 0x1E5DC # ST      R0, 0D111h
	call 0x33030 # BRK
