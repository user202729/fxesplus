#!/bin/sh
if which luajit > /dev/null 2>&1; then
	LUA=luajit
else
	LUA=lua
fi
$LUA ../../CasioEmu/disassembler/disassembler.lua \
	input='rom-emu.bin' output='disas-emu.txt' \
	names='builtins-emu.txt' rom_window='0xd000' entry='1,2,4,9'\
	strict='true' addresses='true' \

# actually entry='1,2,4,5,6,...,21', but deduplicated
