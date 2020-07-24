#!/bin/bash
cd "$(dirname $0)/.."

if which luajit; then
	cmd=luajit
else
	cmd=lua
fi

$cmd CasioEmu/disassembler/disassembler.lua \
	input='991cnx/rom.bin' \
	output='991cnx/disas.txt' \
	entry='1,2,4,5,6,7,8,9,10,11,12,13,14,15,16' \
	strict='true' addresses='true' word_commands='true' rom_window='0xD000' \
	names=<(cat '991cnx/labels' 'labels_sfr') \
	"$@"
