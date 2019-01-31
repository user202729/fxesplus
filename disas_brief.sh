#!/bin/sh

basedir="$(dirname "$0")"

if [[ $# == 0 ]]; then
	input="$basedir/82esp/emu_rom.bin"
	output="$basedir/82esp/_b_emu_disas.txt"
elif [[ $# == 2 ]]; then
	input="$1"
	output="$2"
else
	echo 'Invalid number of arguments'
	exit
fi

"$basedir/disas/bin/u8-disas-brief" "$input" 0 $(wc -c < "$input") "$output"
