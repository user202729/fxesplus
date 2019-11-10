#!/bin/sh
cd "$(dirname $0)"
../disas/bin/u8-disas 'rom.bin' 0 0x40000 '_disas.txt'
