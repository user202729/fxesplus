#!/bin/sh
cd "$(dirname $0)"
if [ ! -f CasioEmu/models/fx570esplus/rom.bin ]; then
	cp -l rom.bin CasioEmu/models/fx570esplus/rom.bin
fi
CasioEmu/emulator/bin/casioemu \
	model=CasioEmu/models/fx570esplus/ \
	script=CasioEmu/emulator/lua-common.lua \
	history=emu-history \
	"$@"
