#!/bin/sh
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx82esplusa/rom.bin ]; then
	cp -l 82espa/rom.bin CasioEmu/models/fx82esplusa/rom.bin
fi
CasioEmu/emulator/bin/casioemu \
	model=CasioEmu/models/fx82esplusa/ \
	script=82espa/lua-emu-init.lua \
	history=82espa/.emu_history \
	"$@"
