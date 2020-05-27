#!/bin/sh
cd "$(dirname $0)"
../disas/bin/u8-disas-brief 'rom.bin' 0 0x40000 '_b_disas.txt'
