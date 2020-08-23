#!/bin/bash
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx991cnx/rom.bin ]; then
	cp -l 991cnx/rom.bin CasioEmu/models/fx991cnx/rom.bin
fi
args=(\
	model=CasioEmu/models/fx991cnx/ \
	script=991cnx/lua-emu-init.lua \
	history=991cnx/.emu_history \
	exit_on_console_shutdown=true \
	"$@"
)
CasioEmu/emulator/build/emulator "${args[@]}" || \
    CasioEmu/emulator/bin/casioemu "${args[@]}"
