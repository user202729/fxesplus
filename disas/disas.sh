#!/bin/sh
cd "$(dirname $0)"
bin/u8-disas '../rom.bin' 0 0x20000 '../disas_real_570es+_1.txt'
