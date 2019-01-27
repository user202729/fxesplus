#!/bin/sh

if [[ $# == 0 ]]; then
	input="82esp/emu_rom.bin"
	output="82esp/emu_brief_disas.txt"
elif [[ $# == 2 ]]; then
	input="$1"
	output="$2"
else
	echo 'Invalid number of arguments'
	exit
fi

disas/bin/u8-disas-brief "$input" 0 $(wc -c < "$input") "$output"
