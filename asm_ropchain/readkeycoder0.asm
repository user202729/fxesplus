home:
reset_all
loop:
getkeycode
set lr
hex_byte
er2 = er0, pop er8
0x8144
[er8]=er2, pop xr8
0x34333231
xr0= 0x0101, 0x8144
line_print
set lr
render
xr0=0x8A88, 0x8A24
strcpy_null
goto loop
