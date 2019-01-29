#!/bin/sh
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx82es_emu/rom.bin ]; then
	cp -l 82es_emu/rom.bin CasioEmu/models/fx82es_emu/rom.bin
fi
CasioEmu/emulator/bin/casioemu \
	model=CasioEmu/models/fx82es_emu/ \
	script=82es_emu/lua-emu-init.lua \
	history=emu-history \
	"$@"
