#!/usr/bin/python3
import sys,os
os.chdir(os.path.dirname(__file__))
sys.path.append('..')
from libcompiler import (
		set_font, set_npress_array, get_disassembly, get_commands,
		read_rename_list, set_symbolrepr,
		to_font,
		process_program
		)

get_disassembly('disas.txt')
get_commands('gadgets')
read_rename_list('labels')
read_rename_list('../labels_sfr')


font='''
x ¿ à á  é í ó ö ü ú ¡  Ó ä  ¯ ³ ¿
. . . .  . . . . . . .  . .  . . .
x ! " #  × % ÷ ' ( ) ⋅  + ,  — . /
0 1 2 3  4 5 6 7 8 9 :  ; <  = > ?
@ A B C  D E F G H I J  K L  M N O
P Q R S  T U V W X Y Z  [ ▫  ] ^ _
- a b c  d e f g h i j  k l  m n o
p q r s  t u v w x y z  { |  } ~ ⊢
𝐢 𝐞 × ⏨  ∞ ° ʳ ᵍ ∠ x̅ y̅  x̂ ŷ  → Π ⇒
ₓ ⏨ ⏨̄ ⌟  ≤ ≠ ≥ ⇩ √ ∫ ᴀ  ʙ ᴄ  ₙ ▶ ◀
⁰ ¹ ² ³  ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁻¹ ˣ ¹⁰ ₍ ₎ ±
₀ ₁ ₂ ₋₁ ꜰ ɴ ᴘ µ 𝐀 𝐁 𝐂  𝐃 𝐄  𝐅 𝐏 ▷
Σ α γ ε  θ λ μ π σ ϕ ℓ  ℏ █  ⎕ ₃ ▂
. . . .  . . . . . . .  . .  . . .
. . . .  . . . . . . .  . .  . . .
. . . .  . . . . . . .  . .  . . .
'''.split()
font[0]=font[0x20]=' '

assert '⁻¹'==font[0xAA]
assert len(font)==0x100,len(font)
set_font(font)


# NOTE: may be incorrect
npress=(
	999,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,
	4  ,4  ,4  ,4  ,4  ,4  ,4  ,4  ,4  ,4  ,4  ,4  ,4  ,100,100,100,
	100,102,100,100,100,2  ,100,100,1  ,1  ,100,1  ,1  ,1  ,1  ,100,
	1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,100,100,100,100,100,100,
	100,2  ,2  ,2  ,2  ,2  ,2  ,100,100,100,100,100,100,100,1  ,1  ,
	100,100,100,100,2  ,100,100,2  ,2  ,2  ,100,100,1  ,100,1  ,100,
	1  ,100,100,2  ,100,4  ,4  ,100,1  ,100,100,100,2  ,2  ,100,100,
	2  ,2  ,2  ,2  ,1  ,1  ,2  ,1  ,100,100,100,100,100,100,100,100,
	100,2  ,2  ,100,100,3  ,3  ,3  ,100,4  ,4  ,1  ,2  ,100,100,100,
	2  ,2  ,2  ,2  ,100,100,100,100,1  ,100,4  ,4  ,100,4  ,100,2  ,
	1  ,1  ,1  ,1  ,100,100,100,100,2  ,100,4  ,4  ,4  ,4  ,1  ,100,
	2  ,2  ,2  ,2  ,100,100,100,100,100,100,100,100,100,100,2  ,2  ,
	100,100,2  ,100,100,100,100,100,100,100,100,100,100,100,100,100,
	100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,
	100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,
	100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,
	)  # the box may be harder to manipulate
set_npress_array(npress)

def get_binary(filename):
	file = open(filename, 'rb')
	result = file.read()
	file.close()
	return result
rom = get_binary('rom.bin')

def get_symbols(rom):
	symbols = [''] * 256
	for i in range(1, 256):
		ptr_adr = 0x148E + 2*i  # referenced at code address 02BBE
		ptr = rom[ptr_adr+1] << 8 | rom[ptr_adr]

		info = rom[0x168E + i]
		symbol_len = info & 0xF
		symbol_type = info >> 4 # if 15 then func else normal

		if symbol_type != 15: ptr += symbol_type

		result = to_font(rom[ptr:ptr+symbol_len])
		if symbol_type == 15: result = result + '('
		symbols[i] = result

	return symbols
symbols = get_symbols(rom)
set_symbolrepr(symbols)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', default='overflow',
		choices=('none', 'overflow', 'loader'),
		help='how will the output be used')
parser.add_argument('-f', '--format', default='key',
		choices=('hex', 'key'),
		help='output format')
args = parser.parse_args()

program = sys.stdin.read().split('\n')

process_program(args, program, overflow_initial_sp=0x8DAE)
