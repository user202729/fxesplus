#!/bin/bash
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx82esplusa/rom.bin ]; then
	cp -l 82espa/rom.bin CasioEmu/models/fx82esplusa/rom.bin
fi
args=(\
	model=CasioEmu/models/fx82esplusa/ \
	script=82espa/lua-emu-init.lua \
	history=82espa/.emu_history \
	exit_on_console_shutdown=true \
	"$@"
)
CasioEmu/emulator/build/emulator "${args[@]}" || \
    CasioEmu/emulator/bin/casioemu "${args[@]}"
