#!/bin/sh
cd "$(dirname $0)/.."
if [ ! -f CasioEmu/models/fx580vnx_emu/rom.bin ]; then
	cp -l 580vnx_emu/rom.bin CasioEmu/models/fx580vnx_emu/rom.bin
fi
args=(\
	model=CasioEmu/models/fx580vnx_emu/ \
	script=580vnx_emu/lua-emu-init.lua \
	history=580vnx_emu/.emu_history \
	exit_on_console_shutdown=true \
	"$@"
)
CasioEmu/emulator/build/emulator "${args[@]}" || \
    CasioEmu/emulator/bin/casioemu "${args[@]}"
