#!/bin/sh
cd "$(dirname $0)/.."

if which luajit; then
	cmd=luajit
else
	cmd=lua
fi

$cmd CasioEmu/disassembler/disassembler.lua \
	input='82es_emu/rom.bin' \
	output='82es_emu/disas.txt' \
	entry='1,2,4,5,6,7,8,9,10,11,12,13' \
	addresses='true' rom_window='0x8000' \
	names='82es_emu/labels' \
	"$@"
