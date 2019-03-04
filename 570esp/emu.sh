#!/bin/sh
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx570esplus/rom.bin ]; then
	cp -l 570esp/rom.bin CasioEmu/models/fx570esplus/rom.bin
fi
CasioEmu/emulator/bin/casioemu \
	model=CasioEmu/models/fx570esplus/ \
	script=570esp/lua-emu-init.lua \
	history=570esp/.emu_history \
	"$@"
