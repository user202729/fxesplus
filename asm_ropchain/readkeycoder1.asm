home:
getkeycode
r0=r1
set lr
hex_byte
er2 = er0, pop er8
0x8154
[er8]=er2, pop xr8
0x34333231
xr0= 0x0101, 0x8154
line_print
set lr
render
xr0=0x8365, 0x8301
strcpy_null
goto home
