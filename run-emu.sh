#!/bin/sh
if [ ! -f CasioEmu/models/fx570esplus/rom.bin ]; then
	cp -l rom.bin CasioEmu/models/fx570esplus/rom.bin
fi
CasioEmu/emulator/bin/casioemu CasioEmu/models/fx570esplus/

