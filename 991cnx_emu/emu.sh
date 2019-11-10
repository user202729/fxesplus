#!/bin/sh
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx991cnx_emu/rom.bin ]; then
	cp -l 991cnx_emu/rom.bin CasioEmu/models/fx991cnx_emu/rom.bin
fi
CasioEmu/emulator/bin/casioemu \
	model=CasioEmu/models/fx991cnx_emu/ \
	script=991cnx_emu/lua-emu-init.lua \
	history=991cnx_emu/.emu_history \
	exit_on_console_shutdown=true \
	"$@"
