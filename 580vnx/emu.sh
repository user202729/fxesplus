#!/bin/bash
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx580vnx/rom.bin ]; then
	cp -l 580vnx/rom.bin CasioEmu/models/fx580vnx/rom.bin
fi
args=(\
	model=CasioEmu/models/fx580vnx/ \
	script=580vnx/lua-emu-init.lua \
	history=580vnx/.emu_history \
	exit_on_console_shutdown=true \
	"$@"
)
CasioEmu/emulator/build/emulator "${args[@]}" || \
    CasioEmu/emulator/bin/casioemu "${args[@]}"
