#!/bin/sh

if which luajit > /dev/null 2>&1; then
	LUA=luajit
else
	LUA=lua
fi

# Patch: if a label name is given for a `l` label, does not prepend
# the context name. Useful when there are too many context errors.
# (actually because CCU8 is too smart and try to reuse common parts)
# Also make '#' starts a comment.
if [ ! -f disassembler-patched.lua ]; then
	cp '../../CasioEmu/disassembler/disassembler.lua' '.'
	patch disassembler.lua disassembler-patch
	mv disassembler.lua disassembler-patched.lua
fi
# if it's present, assume it's correct

$LUA disassembler-patched.lua \
	input='rom-emu.bin' output='disas-emu.txt' \
	names='builtins-emu.txt' rom_window='0xd000' entry='1,2,4,9'\
	strict='true' addresses='true' \

# actually entry='1,2,4,5,6,...,21', but deduplicated

