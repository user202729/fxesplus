This is not often used.

# Note

See `builtins` and `570es+ funcs.txt` for more info.

# Snippets

## {RT} Copy exactly 1 byte in less code

	015232   80 94              L       R4, [ER8]
	015234   1E F8              POP     ER8
	015236   1F FE              RT

	014604   E1 90              ST      R0, [ER14]
	014606   C1 D8              ST      R8, 01h[FP]
	014608   C2 D7              ST      R7, 02h[FP]
	01460A   C3 D6              ST      R6, 03h[FP]
	01460C   C4 D5              ST      R5, 04h[FP]
	01460E   C5 D4              ST      R4, 05h[FP]
	014610   1F FE              RT

15232: "2 o 1"
1460e: "cs14 Fvar 1"

4	pop er8
2	[er8]
4	l r4, er8
2	<- er8
4	pop er14
2	[er14]
4	st r4, 5[fp]

Strictly require LR correct. 22 bytes (save only 2 byte, unfortunately)

In extreme cases this may be needed.

## Set ER2 = 0x0001

(also set r0=0)

	er2 = 0x0101
	call 0x1852c # see below

Where:

	01852C   FF 13              ADD     R3, #255
	01852E   F3 C8              BC      NE, 18516h
	018530   00 00              MOV     R0, #0
	018532   8E F2              POP     PC

# Misc

## Secondary character method

Change byte `0x8123` (570es+) to non-zero. (math mode only)

## Arithmetic functions

Format:

	struct number {
		char[10] data;
	};
	using arithmetic_fn = void(number& p0, const number& p1);

Function is in in segment 1.
`&p0` (`er0`) and `&p1` (`er1`) are near pointers in segment 0.
Result is written to `p0`.


	00	4796	[ unknown, invoked twice before frac for num & denom & once after frac for result. Does not change the result. Unary. ]
	01	30b2	P (stat)
	02	3152	Q (stat)
	03	316c	R (stat)

	03	373c	det (matrix)

	09	3404	+ (matrix)
	0a	34be	- (matrix)
	0b	34c6	* (matrix * scalar)
	0c	3532	/ (matrix / matrix)
	0f	35de	* (matrix * matrix)

	08	a716	abs
	09	483c	Rnd
	0c	a88e	sinh
	0d	a87c	cosh
	0e	a86a	tanh
	0f	a858	sinh-1
	10	a846	cosh-1
	11	a834	tanh-1
	12	a632	e^
	13	a61e	10^
	14	aadc	sqrt
	15	a646	ln
	16	abcc	cuberoot (^1/3)
	17	4de6	sin
	18	4df0	cos
	19	4e86	tan
	1a	a8c4	sin-1
	1b	a8b2	cos-1
	1c	a8a0	tan-1
	1d	a65a	unary log
	20	a4ee	binary log
	21	4cd8	Pol (store first value to result, second value to somewhere else)
	22	4ce0	Rec ( " )
	28	4ab2	+
	29	4abe	-
	2a	4aca	*
	2b	4ad6	/
	2e	a516	P (Permutation)
	2f	a502	C (Combination)
	34	b1b8	(-)
	39	4bd6	frac
				weirdly, when the denominator is 0 it does not return error (f3). Instead it does not change r0. Binary.
				Even more weirdly this can be used as ternary function (mixed fraction) with 2 param = num & denom without any indicator where is integral part
	3a	4a7e	pow (also support complex)
	3b	11e0	nth-root (p1 ^ (1 / p0))
	3d	3190	>t (stat)
	40	6d8e	inverse (^-1)
	41	6d6c	square (^2)
	42	6d30	cube (^3)
	43	4d00	%
	44	a5a6	! (factorial)
	45	4d12	deg
	46	4d16	rad
	47	4d1a	grad
	48	ae26	abs (complex)
	4b	4b1c	+ (complex)
	4c	4b30	- (complex)
	4d	4b44	* (complex)
	4e	4ba8	/ (complex)
	4f	48cc	(-) (complex)
	50	4b08	inverse (complex)
	51	717c	square (complex)
	52	7150	cube (complex)
	54	333a	RanInt#

# Disassembly

(some functions are extremely trivial.
Nevertheless it doesn't cause any harm by keeping them)

## f\_02C04 (`num_output_print`)

Prototype: `void(num*)`.

Allocate 26 bytes for the number string representation (including null byte)
Compute the x-coordinate to draw as `96-6*len`.

## f\_03486

(read Pd number, store to R0)

	push LR
	push QR8

	byte [0F042h] = 0
	byte [0F041h] = 0
	word [0F046h] = 0 ; byte [0F046h] = KO
	word [0F044h] = 0FC7Fh
	R15 = 0
	ER10 = 0200h

	outer:
	for (R8 = 3; R8 != 0; --R8, ER10 >>= 1) {
		34B4:
		R12 = 0
		R14 = 0
		word [0F046h] = ER10  ; can be 0200h, 0100h or 0080h
		nop

		for (R13 = 3; R13 != 0; --R13) {
			if (KI.7 == 0)
				++R12
		}

		if R12 >= 2			; repeat R13 = 3 times, R12 can be 0, 1, 2 or 3. R14 calculated by majority of read data
			R14 = 1

		R0 = R8 - 1  ; 2, 1 or 0
		R15 += (R14 << R0)

		word [0F046h] = 0
		R12 = 3
		R13 = 255

		do {
			while (KI.7) {
				--R12;
				if (R12 == 0) continue outer;
			}

			; reach here if KI.7 is off before it is read 3 times in the above loop
			R12 = 3
			--R13
		} while (R13 != 0);
		; wait until KI.7 is off, or when counted to 3*255.
	}
	call 0:3518		; word [0F044h] = 0FF80h
	return r15

	pop qr8
	pop pc

## f\_154F2

Copy function for number. `void(number* x, number* y)`
`x` is at `er0`, `y` is at `er12`. (`bp`, not `er2`)
Change no register.

	Backup r0..r11
	*x = *y
	if ([0x80f9] == MODE_CMPLX /* 196 */)
		*(x+1) = *(y+1);


## f\_04E50

`strcpy`

Copy null-terminated string from [ER2] to [ER0].
When invoked to copy from input to cache (in basic overflow),
return to 00:28FA [re 2768]; when PC = 4e66, (before 6 register
pop's), SP = 8D9E.

## f\_04C30

Convert hexadecimal number in R0 to ASCII, stored in ER0.
Used by checksum procedure.

	R1 = R0 & 0xF;
	if (R1 >= 10) R1 += 0x37; else R1 += 0x48;
	R0 = R0 >> 4;
	if (R0 >= 10) R0 += 0x37; else R0 += 0x48;
	return ER0;

## f\_096EA

`strcat`

Append a null-terminated string to another null-terminated string.

## f\_05A4E

Convert output character to its name.

## f\_02B10

Write content (Bin|Oct|Dec|Hex) to screen.

	Let sub_mode = [80FAh];
	R0 = sub_mode >> 2;
	ER0 = ((word) R0) << 2;
	ER2 = 2CC0h + ER0;
	R0 = 78, R1 = 12;
	func_300C(); ; take R0, R1, ER2
	return;

## f\_02E7A
Write 1 line of contents (pointed to by ER2) to screen at position (x = R0, y = R1)
If call `f_2e78` then x = 0.

## f\_1444C

Note: `(R4 -> R0)` is the concatenated in little-endian of R4 to R0,
just like `XR0 = (R3 -> R0)`.

`(R4 -> R0) <<= 7` means

	SLLC R4, #7
	SLLC R3, #7
	SLLC R2, #7
	SLLC R1, #7
	SLL  R0, #7

Code:

	byte &sub_mode = [080FAh];

	Backup R4 ... R15;
	[ER2] = (byte) 0;
	if ([ER0] >= 16) return;
	ER12 = ER0; ER14 = ER2;
	call 01h:0459Ch; ; get data from variable?
	R9 = sub_mode;
	if (R9 == 9) {
		cmd_144DC:
		EA = ER14;
		if (R10 != 0) { ; R10 ?
			[EA+] = R10 = 96d; ; 96d = 60h = negative sign
		}
		cmd_144E6:
		ER0 = ER4;
		ER2 = ER6
		R4 = R8
		ER6 = 10
		R8 = 4
		R9 = 15
	} else { ;  mode is expected to be Hex, Bin or Oct
		Backup R9 for {
			cmd_1446E: call 01h:04612h;
		} ; perhaps this is Dec-to-Hex converter
		if (flag LT) return;

		; cmd_14476:
		EA = FP; ; as expected, ER14 = FP should point on stack
		R6 = 16, R7 = 1;
		R8 = R9;
		if (R9 == 1) { ; Bin
			;cmd_14482:
			(R4, R3) = (R1, R0);
		} else {
			; cmd_14488:
			unsigned R8 >>= 3;
			R8 += 3;
			R6 = 11;
			if (R9 != 7) { ; so 15 and other bases (Hex)
				cmd_14492:
				R6 = 8;
				(R4 -> R1) = (R3 -> R0); ; corresponding to shiftleft of 8 places
			} else { ; Oct
				cmd_1449E:
				(R4 -> R0) <<= 7;
				Reset bit R4.7;
			}
		}
	}
	do {
		; cmd_144AA:
		R5 = high_byte(ER4 << R8) & R9;
		if (R5 != 0 || R7 != 0) goto cmd_144B8;

		if (R6 != 1) goto cmd_144C4;

		cmd_144B8: R7 = 1;
		R5 += '0'; ; 030h
		if (R5 >= 03Ah) { ; R5 > '9'
		; cmd_144C0:
			R5 += 126d; ; equal to 'hex_A' (B8) - '0' + 10
		}
		[EA+] = R5; ; this command write contents to 0:8D9E, in stack
		; going to be copied to other positions and displayed on the screen

		cmd_144C4:
		--R6;
		if (R6 == 0) break;
		; cmd_144C8:
		(R4 -> R0) <<= R8;
	} while (true);
	; cmd_144D2: BC      AL, 144AAh

	[EA+] = R0; ; it is expected that after several times of shifting,
	; R0 is 0, but there may be exceptional cases
	return;

## f\_047F2

{RT} Return true if there is a key pressed.

	[0F046h] = 07Fh
	R2 = [0F040h]     // with a delay of 2 clock cycles
	R0 = (R2 != 0FFh) // if (R2 == 0FFh) R0 = 0; else R0 = 1;

## f\_046CC

Return value of bit 080F4h.7. `(void)->er0`.

	if (080F4h.7 == 0) {return 0};
	return 1;

## f\_0312C

Copy screen buffer to hardware screen.

	Backup XR4, QR8;
	ER0 = 087D0h;
	PUSH ER0;

	ER2 = 0F800h;
	R0 = 32;
	do {
		POP EA;
		XR4 = [EA+]; QR8 = [EA+];
		PUSH EA;

		EA = ER2;
		[EA+] = XR4; [EA+] = QR8;
		ER2 += 010h;
		--R0;
	} while (R0 != 0);
	POP ER0

## f\_07EF6

{RT} `memcpy`. (return `dest`)

`char*(char* dest @ er0, char* source @ er2, unsigned length @ stack)`

	char* result = dest // er8
	// dest and source is moved to er4 and er12 resp.
	while (length > 0) {
		[dest++] = [source]
		++source
		length -= 1
	}
	return result


------------

Unrefactored parts below.

------------

	------------------------------
	disas of 0:0BB8Eh im (0:0B2E0h re)
	; get pressed button, store to *(param0) and *(param0+1)

	[[Recursive]]
	Backup XR8, XR4; ; R4 -> R11
	ER8 = ER0;
	R10 = #1
	ER6 = 0F046h;
	ER2 = 0F040h;
	R1 = R4 = 1;

	cmd_BBA4:
	do {
		[0F046h] = R1; ; ER6 = 0F046h. R1 = 1<<0 ; 1<<1 ; ... ; 1<<6
		R0 = [0F040h]; ; without any clock-cycle delay
		if (R0 != #255) { ; ER2 = 0F040h;
			cmd_BBAC:
			[ER8+0001h] = R1;
			[ER8] = (R0 = ~R0);  ; ER8 = input
			goto finalize;  ; return 1 (without executing R10 = 0)
		}

		unsigned(R1) <<= 1; ; SLL
		++R4;
	} while (R4 <= #7); ; at first R4 = 1, each iteration ++R4, therefore the loop is executed 7 times.

	R10 = 0  ; return 0 (with executing R10 = 0) => no button pressed

	finalize:
	cmd_BBC0:
	BL      00h:048F6h ; zero 0F046h (and R2)
	MOV     R0, R10
	return;

------------------------------

disas 00h:0bbcch im (00h:0B31Eh re)

Takes ER0 as input.

[[Recursive]]
	Backup R4 -> R13; ; XR8, XR4, ER12
	ER8 = ER0; ; input
	R12 = R0 = 1;
	R4 = 0;
	ER6  = 0F046h;
	ER10 = 0F040h;
	R5 = 1;

	cmd_BBE6:
	do {
		func_474C(ER0 = 000Dh);         ; im 474c = hardware function
		[0F046h] = R0 = [ER8+0001h];  ; 1-byte; ER6 == 0F046h; ER8 = input
		R0 = ~[0F040h]; ; use ER10 = 0F040h;

		;; R0 is backup'd to R13 around this function-call, but that is unimportant
		func_48F6()    ; 48f6 im ; zero 0F046h (and R2)

		R0 &= [ER8]; ; use R1 = [ER8] as temporary
		; ER8 = input. Therefore after this command R0 = (~[0F040h]) & [input]

		if (R0) {
			cmd_BC04: ++R4;    ; => only return 1 if this command is executed exactly 5 times. <=> all the times
		}
		++R5;
	} while (R5 <= 5); ; loop repeated for 5 times
	; This is to filter possible noise by repeat reading the value from the keyboard 5 consecutive times

	cmd_bc0e: if (R4 != 5) {
		R12 = R0 = 0; ; return 0 => no key pressed
	} ; else return 1 (R12 = 1 above)

	return R0 = R12;

---- 0:b148 (approx) ----

Function used for reading key. [real code]



; b148 re perhaps = ba6c im
[0811Ch] = R0;
[FP-08h] = R0 = #1
[FP-03h] = [FP-04h] = R0 = #172

;LOOP:
	00B156   E5 F0              MOV     ER0, ER14
	00B158   D0 E0              ADD     ER0, #-48         ; that is -30h.
	00B15A   01 F0 26 B2        BL      00h:0B226h        ; equal to what? proven 0:BAEA. / does not affect FP
	00B15E   40 81              MOV     R1, R4            ; where does R4 come from?
	00B160   FF 14              ADD     R4, #255
	00B162   00 71              CMP     R1, #0
	00B164   0C C8              BC      NE, 0B17Eh
	00B166   01 F0 CC 46        BL      00h:046CCh        ; R0 = 80F4h.7

	cmd_b16a:
	if (r0 != 0) { ; there is a 'return' in this loop
		cmd_b16e:
		00B16E   01 F0 C0 46        BL      00h:046C0h        ; Otherwise clear all other bits in 80F4h
		00B172   E8 A0 CE FF        L       ER0, -0032h[ER14] ; ER14 = FP.
		00B176   E9 A0 CC FF        ST      ER0, -0034h[ER14] ; Where does those addresses come from?
		00B17A   83 90              ST      ER0, [ER8]        ; but that appear to come before ER0 (fed into re 0:B226 above) for 2 - 4 bytes.
		00B17C   0F CE              BC      AL, 0B19Ch

	}

	; func_4640 correspond to important hardware function (0:474C) in real calculator
	func_4640(ER0 = 0013h)

	00B184   E5 F0              MOV     ER0, ER14         ; fortunately no recursive call, but a lot of modification to F*** addresses
	00B186   CE E0              ADD     ER0, #-50
	00B188   01 F0 92 B2        BL      00h:0B292h

	cmd_b18e: if (R0 != 0) B 0B156h        ; loop
;ENDLOOP (to b190)

00B190   01 00              MOV     R0, #1
00B192   FC D0              ST      R0, -04h[FP]
00B194   FD D0              ST      R0, -03h[FP]
00B196   00 00              MOV     R0, #0
00B198   F8 D0              ST      R0, -08h[F0]
cmd_B19A   29 CE              BC      AL, 0B1EEh

cmd_b1ee:
outer: while (true) {
	00B1EE   01 F0 D2 47        BL      00h:047D2h             ; 47d2 re = 48de im : byte ptr [0F042h] = 0FFh
	00B1F2   01 F0 E2 47        BL      00h:047E2h             ; 47e2 re = 48ee im : byte ptr [0F046h] = 07Fh
	00B1F6   E2 CE              BC      AL, 0B1BCh

	; infinite loop: perhaps wait for user input
	outer: while (true) {
		cmd_B1BC:
		func_B226h (ER0 = ER14 -48);                         ; BAEA im??? also called on RE[00B15A]

		; hardware function. call with identical parameter to IM[00474C] at IM[00BA9A]
		func_4640(ER0 = 129Ah);                              ; perhaps this function, when called with ER0 = 129A, wait for a period of time

		cmd_B1CC:
		inner: do {
			func_46A6();        	 ; 047b2 emulator = read_f014. Perhaps the same on real calculator - read f014
			if (R0.1 is set) {          ; there is a button pressed, reported by interrupt
				cmd_B1D4:
				call 0:47F2h;                           ; See disassemble above. Hardware function, modify R0 to 0 or 1.
				; perhaps correspond to IM[048fe] => read rcc (real calculator code) partially, correct with high probability

				if (R0) break outer; ; to cmd_B1F8 <perhaps when there is a input key>
				; R0 iff R2 != 0FFh
				; send current to all KO, then read from KI

				; IM[04792] : set calculator to stop mode with [0F014h] &= ~02h
				func_4686();

				; the following command will be executed if:
				; return value of RE[047F2] is R0=0     AND
				; (return value of RE[046A6]).1 is set (above)
				continue inner;        ; inner loop                              ; 00B1E0   F5 CE              BC      AL, 0B1CCh
			}
			break inner;              ; if there is no button pressed, increase RTC (as it is called)
		} while(true); ; this loop will break unless `continue inner` is executed

		++ (word) [08224h];      ; perhaps equivalent to IM[00BAAE]
		continue;           ; redundant continue, written for clarity ; 00B1EC   BC      AL, 0B1BCh
	}

	cmd_B1F8: BL      00h:047EAh             ; 48f6 im ; zero 0F046h (and R2)
	BL      00h:047DAh				; im 48e6 : zero 0F042h (and R0)

	func_4640(ER0 = 1);
	ER0 = ER14 -34h;               ; input parameter
	BL      00h:0B2E0h             ; bb8e im, offset = 8ae
	if (R0 == 0) continue outer;

	cmd_B212: ER0 = ER14 -34h;
	BL      00h:0B31Eh             ; bbcc im, offset = 8ae
	if (R0 == 0) continue outer;

	break; ; iff there is a button pressed
}

cmd_B21E: [ER8] = ER2 = [ER14-0034h];  ; this actually store 2 bytes to (byte ptr [ER8]) and (byte ptr [ER8+1])
cmd_B224: goto cmd_0B19C;

cmd_B19C:
BL      00h:047EAh ; 48f6 im ; zero 0F046h
[080F2h] = [ER14-0034h];
ER2 = ER14 -1Ch;
ER0 = [FP-06h];
00B1AE   01 F0 B2 B3        BL      00h:0B3B2h            ; bc60 im = "handle button press stored in [ER8] and [ER8+1]".
00B1B2   1E F4              POP     ER4
00B1B4   1E F8              POP     ER8
00B1B6   EA A1              MOV     SP, ER14
00B1B8   1E FE              POP     ER14
00B1BA   8E F2              POP     PC


; ----------------- End of function -----------------

void f_0B654 {
	push lr
	backup er14
	uint16_t x @ (er14-2)

	do {
		f_0B0C6(er0 = &x)
		f_0B410(er0 = &x, er2 = 0x2056)
	} while (r0 != 233); 233 is probably the value of shift key

	return;
}




---------------------------------------
void f_0B0C6 (er0) {
	Backup: er14
	Allocate 52d bytes:
		uint16_t a4 @ (fp - 52)
		uint16_t a2 @ (fp - 50)
		void x2 @ (fp - 48)

		void x1 @ (fp - 28)

		uint8_t b4 @ (fp - 8)
		bool b1 @ (fp - 7)
		uint16_t a3 @ (fp - 6)

		uint8_t b2 @ (fp - 4)
		uint8_t b3 @ (fp - 3)
		uint16_t a1 @ (fp - 2)


	Backup: er8, er4
	mov er8, er0
	a1 = 0x04ab
	r4 = 0x30 ; r4 = loop variable (below)
	if (f_046d4() != 0) mov r4, 0xEE ; f_046d4() = 080F4h.3
	a2 = er0 = [d_080F2] ; [d_080F2] : probably last held key mask
	b1 = f_0B3EC() ; (probably) cursor flashing

	[d_0811B] = [d_08117]
	[d_0811C] = 1
	[d_0811D] = 0
	er2 = &a3
	l r1, [d_08115] ; cursor.y
	l r0, [d_08114] ; cursor.x
	bl f_03158 ; probably putchar (or not)
	f_0B370(er0 = &x1, er2 = a3)

	if (b1) { ; probably cursor flashing
		l r2, [d_08116]
		l r1, [d_08115] ; cursor.y
		l r0, [d_08114] ; cursor.x
		bl f_02EBA
	}

	f_0B370(er0 = &x2, er2 = a3)
	byte [d_0811D] = 1
	byte [d_0811C] = 0
	b4 = 1
	b3 = b2 = 172

	do {
		er0 = &x2
		bl f_0B226
		; short-circuit
		if (!(r4-- || f_046CC() == 0)) {
			bl f_046c0
			[er8] = a4 = er0 = a2
			goto __return
		}

		f_4640(er0 = 0x0013)
	while (f_0B292(er0 = &a2) != 0); // while key [a2] is still held (?)

	b3 = b2 = 1
	mov r0, 0
	st r0, b4
	bc al, .l_128

	.l_128: {
		bl f_047D2
		bl f_047E2

		outer: while(1) {
			er0 = &x2
			bl f_0B226
			f_04640(er0 = 0x129A)
			inner: while (1) {
				if (f_046A6().1 == 0) break inner; // cpu woken because of timer
				if (f_047F2()   != 0) break outer;
				bl f_04686
			}
			++ uint16_t [d_08224] ; timer
		}

		bl f_047EA
		bl f_047DA
		f_04640(er0 = 0x0001)

	} while (f_0B2E0(er0 = &a4) == 0 || f_0B31E(er0 = &a4) == 0)

	l er2, *(int16_t*)&a4
	st er2, [er8]
	bc al, __return

	__return:
		bl f_047EA
		[d_080F2] = a4
		er2 = &x1
		er0 = a3
		bl f_0B3B2
		pop er4
		pop er8
		mov sp, er14
		pop er14
		pop pc

----------------------------------------

bool f_0B3EC (void):   ; 1-byte bool
	if (int8_t[d_080DD] != 0) {
		mov r0, 0 ; cursor stop flashing
		rt
	}
	if (int8_t[d_080FB] != 0) {
		mov r0, 0
		rt
	}
	if (int8_t[d_080FE] != 1) {
		mov r0, 0
		rt
	}
	mov r0, 1
	rt

; Return bool(int8_t[d_080DD] == 0 && int8_t[d_080FB] == 0 && int8_t[d_080FE] == 1)
; Probably (cursor is flashing?)

---------------------------------------

	// out_adr: er0, in_adr: er2. As usual for functions, only modify r0..r3.
	f_0B370 (near int8_t* out_adr, near int8_t* in_adr) {
		allocate 2 bytes: (fp - 2 is not used)
			uint8_t a @ (fp - 1)
	
		er10 = in_adr
		for(a = 0; a < uint8_t(*d_08117); ++a){
			// d_08117: probably char height
			out_adr[2*a] = int8_t[er10]
			out_adr[2*a+1] = int8_t[er10+1]
			er10 += 16 ; real screen byte width
		}
	}

-----------------------

; draw_char?

f_02EBA (uint8_t col@r0, uint8_t row@r1, uint8_t chr@r2) {
	push lr
	backup r4 .. r15
	allocate 21 bytes:

		void u1 @ (er14 - 21)
		int16_t w4 @ (fp - 12)
		int16_t w5 @ (fp - 10)
		near ptr tmp_screen_pos @ (fp - 8)
		int8_t b3 @ (fp - 6)
		int8_t b2 @ (fp - 5)
		near ptr screen_lastbyte @ (fp - 4)
		int8_t b4 @ (fp - 2)
		int8_t screen_width @ (fp - 1)

	local:
		near ptr screen_pos @ er10


	if (col > 95u || int8_t(row) >= 32) goto __return;

	if (int8_t [d_0811D] == 0) {
		screen_width = 16
		screen_lastbyte = 0xf9ff
	} else {
		screen_width = 12
		screen_lastbyte = 0x894f
	}

	l r3, [d_0811B]
	if (r3 == 6) {
		b3 = 4
		b2 = 4
	} else {
		b3 = 6
		b2 = 2
	}
	if (r3 == 7 && chr < 32) {
		++ r3  ; font size = 6/7 (7/8) for small font in case of diacritics
		-- row
	}
	push r3
	mov er6, er0
	mov r0, r2
	mov er2, &u1
	bl f_02FEC
	st er0, w4
	mov r12, 34
	mov r13, 0
	mov er0, er6
	mov er2, &tmp_screen_pos
	bl f_03158
	screen_pos = tmp_screen_pos
	mov r9, r0
	mov r1, 0
	l r7, d_01C64[er0]
	add r4, r6
	mov r5, 0
	mov r0, r4
	and r0, 7
	l r6, d_01C6C[er0]
	pop r0
	-- r0
	st er0, w5
	do {

		if (r9 == 0) {
			mov er0, screen_pos
			mov er2, er12
			push r6
			bl draw_byte
			pop r0
		} else {
			l r0, b2
			if (r9 <= r0) {
				r0 = r7 & r6
			}
			r8 = ([er12] >>> r9) & r7
			mov er0, screen_pos
			b4 = r8
			mov er2, &b4
			push r7
			bl draw_byte
			pop r0
			l r0, b2
			add r0, 1
			if (r0 <= r9) {
				r8 = ([er12] << (8 - r9)) & r6
				er0 = screen_pos + 1
				st r8, b4
				mov er2, &b4
				push r6
				bl draw_byte
				pop r0
			}
		}
		screen_pos += (uint16_t) screen_width
		if (screen_pos > screen_lastbyte) goto __return
		er0 = w5
		if (r1 == 0) {
			l er12, w4
		} else {
			add er12, 1
		}
		++r1
		w5 = er0
	} while (r1 <= r0);

	__return:
	mov sp, er14
	pop qr8
	pop xr4
	pop pc


; f_030BE. See funcnames

void draw_byte (near uint8_t* ptr1 @ er0, near uint8_t* chr @ er2, uint8_t mask @ sp+0) {
	local uint8_t r14 @ l_char, uint8_t r15 @ l_mask

	backup er14

	er14 = 0x7824
	add er14, ptr1
	bc ge, __return ; ge <-> !carry <-> er14 + er0 <= 0xFFFF <-> er0 <= 0xFFFF - 0x7824 <=> ptr1 <= 0x87DB [correct?]
	;  if (ptr1 <= 0x87DB) goto __return
	mov er14, sp
	ea = ptr1
	r0 = [chr]
	if (mask != 0) r0 &= mask;
	l_char = r0
	l_mask = mask
	switch (byte [d_0811C]) { ; drawing mode?
	case 0: ; draw on (may outside of mask)
		[ea] = ([ea] & ~l_mask) | l_char
		break
	case 4: ; draw on (in mask), remove background at mask
		[ea] = ([ea] & ~l_mask) | (l_mask & ~l_char)
		break
	case 1: ; write over, keep background
		[ea] |= l_char
		break
	case 2: ; [ea] = ([ea] & ~l_mask) | ([ea] & l_char) -> clear screen then write if screen has already -> ????
		[ea] &= (l_char | ~l_mask)
		break
	default: ; xor
		[ea] ^= l_char
		break
	}
	pop er14
	rt
}

--------------------------------------------------------------
; (probably) retrieve key-value from key-mask
; Let csb(x) be number of significant bit of x.
; Return int8_t at r0
; keymask decay to a pointer
(uint8_t @ r0) f_0B410 (near uint8_t[2] keymask @ er0, uint8_t[] keyvalues @ er2) {
	backup xr8 ; use er8 = keymask, er10 = keyvalues
	r2 = [keymask]
	r3 = r0 = [keymask+1]
	if (r0 == 0 || r2 == 0) {
		return 0
	}

	r1 = 0
	while (r2 > 0) {
		++r1
		r2 >>>= 1
	} ; this calculate csb(r2)
	; can be written as:

;	for (r1 = 0; r2 > 0; r2 >>>= 1) {
;		++r1;
;	}

	r2 = r1 ; now, r2 = csb(keymask[0]), which is not zero because of the condition above

	r1 = csb(r3) ; with csb defined above

	r0 = keyvalues [ (--r2) << 3 + (r1 - 1) ]
	__return:
		pop xr8
		rt
	}


--------------------------------------------------------------
; keymask_t is used quite often. It can be declared as
;	struct keymask_t {
;		uint8_t ki @ +0
;		uint8_t ko @ +1
;	}
; or
;	using keymask_t = uint8_t[2]
; always decay to near uint8_t*
uint8_t f_0B292(uint8_t[2] keymask @ er0) {
	backup xr4, er12, er8
	; er8 = keymask
	mov r5, 0
	er6 = 0xF046
	er12 = 0xF040
	[d_0F046] = keymask[1]

	; Can convert to for-loop because the first iteration always lead to valid condition
	; (do-while -> while -> for)
	for (r4 = 1; r4 <= 10; ++r4) {
		if (keymask[0] & ~ byte[er12]) {  ; er12 = &KI
			mov r5, 1
			break
		}
		f_04640(er0 = 13)
	} ; the programmers seems to like loop from 1 to n instead of from 0 to n-1

	byte [er6] = 0 ; KO
	if (r5 == 0) {  ; no key pressed
		f_046C4()  ; byte[d_080F4] = 0
	}
	return r5
}
--------------------------------------------------------------
void f_04640(uint16_t time @ er0) {
	er2 = time
	lea [d_0F024]
	mov er0, 1
	st r0, [ea+]    ; 0F024 = 1
	st r1, [ea]     ; 0F025 = 0
	lea [d_0F022]
	mov r0, 0
	st r0, [ea+]    ; 0F022 = 0
	st r0, [ea]     ; 0F023 = 0
	lea [d_0F020]
	st lower_byte(time), [ea+]  ; 0F020 = lb(time)
	st upper_byte(time), [ea]   ; 0F021 = ub(time)
	lea [d_0F025]
	mov r0, 1
	st r0, [ea]      ; 0F025 = 1
	lea [d_0F014]
	mov r0, 0
	st r0, [ea+]  ; 0F014 = 0
	st r0, [ea]   ; 0F015 = 0
.l_082:
	lea [d_0F008]
	mov r2, 80
	mov r3, 160
	st r2, [ea]   ; 0F008
	st r3, [ea+]  ; 0F008
	mov r0, 2
	st r0, [ea]   ; 0F009
	nop
	nop
.l_096:
	rt
}

--------------------------------------------------------------


--------------------------------------------------------------
f_045EE:
	l r0, [d_080DD]
	bc ne, .l_096
*******
.l_096:
	rt
*******
	bl f_02D38
	mov r0, 156
	mov r1, 0
	push er0
	mov r0, 208
	mov r1, 135
	mov r2, 120
	mov r3, 0
	add er0, er2
	mov r2, 16
	mov r3, 31
	bl f_07EF6
	pop er0
	bl f_0312C
	mov r0, 136
	mov r1, 19
	bl .l_052
*******
.l_052:
	mov er2, er0
	lea [d_0F024]
	mov er0, 1
	st r0, [ea+]
	st r1, [ea]
	lea [d_0F022]
	mov r0, 0
	st r0, [ea+]
	st r0, [ea]
	lea [d_0F020]
	st r2, [ea+]
	st r3, [ea]
	lea [d_0F025]
	mov r0, 1
	st r0, [ea]
	lea [d_0F014]
	mov r0, 0
	st r0, [ea+]
	st r0, [ea]
.l_096:
	rt
*******
	mov er0, 3
	st r0, [d_0F031]
	st r1, [d_0F00A]
	lea [d_0F010]
	mov er2, 0
	st er2, [ea+]
	bl f_047DA
	bl f_047EA
	bl .l_082
	b f_04834

--------------------------------------------------------------
[Partial] Core function used for calculating. -> process operators

f_14EB4 (???) {

		push lr                        ; 14EB4
		if (r1 == 0x75) r1 = 0x2d;
		mov r5, 1 (01)                 ; 14EBC
	.l_00A:
		mov r0, 0 (00)                 ; 14EBE
		cmp r1, 13 (0d)                ; 14EC0
		bc eq, .l_018                  ; 14EC2
		cmp r1, 14 (0e)                ; 14EC4
		bc eq, .l_018                  ; 14EC6
		cmp r1, 47 (2f, '/')           ; 14EC8
		bc ne, .l_024                  ; 14ECA
	.l_018:
		bl f_15546                     ; 14ECC
		bc ge, .l_072                  ; 14ED0
	.l_01E:
		bl f_15596                     ; 14ED2
		pop pc                         ; 14ED6
	.l_024:
		cmp r1, 119 (77, 'w')          ; 14ED8
		bc eq, .l_066                  ; 14EDA
		cmp r1, 120 (78, 'x')          ; 14EDC
		bc eq, .l_066                  ; 14EDE
		cmp r1, 15 (0f)                ; 14EE0
		bc lt, .l_0A6                  ; 14EE2
		cmp r1, 37 (25, '%')           ; 14EE4
		bc le, .l_066                  ; 14EE6
		cmp r1, 48 (30, '0')           ; 14EE8
		bc lt, .l_03C                  ; 14EEA
		cmp r1, 95 (5f, '_')           ; 14EEC
		bc lt, .l_066                  ; 14EEE
	.l_03C:
		cmp r1, 101 (65, 'e')          ; 14EF0
		bc eq, .l_056                  ; 14EF2
		cmp r1, 102 (66, 'f')          ; 14EF4
		bc eq, .l_066                  ; 14EF6
		cmp r1, 110 (6e, 'n')          ; 14EF8
		bc ge, .l_066                  ; 14EFA
		cmp r1, 107 (6b, 'k')          ; 14EFC
		bc ge, .l_06A                  ; 14EFE
		cmp r1, 100 (64, 'd')          ; 14F00
		bc eq, .l_068                  ; 14F02
		cmp r1, 42 (2a, '*')           ; 14F04
		bc eq, .l_068                  ; 14F06
		bc al, .l_072                  ; 14F08
	.l_056:
		cmp r5, 1 (01)                 ; 14F0A
		bc eq, .l_068                  ; 14F0C
		l r3, [er12]                   ; 14F0E
		srl r3, 4 (04)                 ; 14F10
		cmp r3, 6 (06)                 ; 14F12
		bc ne, .l_06A                  ; 14F14
		mov r2, 2 (02)                 ; 14F16
		pop pc                         ; 14F18
	.l_066:
		or r0, 7 (07)                  ; 14F1A
	.l_068:
		or r0, 3 (03)                  ; 14F1C
	.l_06A:
		or r0, 1 (01)                  ; 14F1E
		bl f_15546                     ; 14F20
		bc lt, .l_01E                  ; 14F24
	.l_072:
		cmp r1, 119 (77, 'w')          ; 14F26
		bc eq, .l_0AE                  ; 14F28
		cmp r1, 120 (78, 'x')          ; 14F2A
		bc eq, .l_08E                  ; 14F2C
		cmp r1, 116 (74, 't')          ; 14F2E
		bc eq, .l_08E                  ; 14F30
		cmp r1, 35 (23, '#')           ; 14F32
		bc lt, .l_0AE                  ; 14F34
		cmp r1, 50 (32, '2')           ; 14F36
		bc le, .l_08E                  ; 14F38
		cmp r1, 100 (64, 'd')          ; 14F3A
		bc lt, .l_0AE                  ; 14F3C
		cmp r1, 102 (66, 'f')          ; 14F3E
		bc gt, .l_0AE                  ; 14F40
	.l_08E:
		add r5, 255 (ff)               ; 14F42
		bc ne, .l_0AE                  ; 14F44
		push r1                        ; 14F46
		mov er0, er12                  ; 14F48
		add er0, 20 (14)               ; 14F4A
		bl f_154F2                     ; 14F4C
		mov er2, er12                  ; 14F50
		bl f_151D6.l_02E               ; 14F52
		pop r1                         ; 14F56
		bc al, .l_00A                  ; 14F58

	.l_0A6:
		mov r0, 255 (ff)               ; 14F5A
		bl f_15546                     ; 14F5C
		bc lt, .l_01E                  ; 14F60
	.l_0AE:
		cmp r1, 3 (03)                 ; 14F62
		bc ne, .l_0B6                  ; 14F64
		b .l_242                       ; 14F66
	.l_0B6:
		l r0, [d_08121]                ; 14F6A
		l r2, [er12]                   ; 14F6E
		l r3, 20 (14)[er12]            ; 14F70
		cmp r2, 144 (90)               ; 14F72
		bc ge, .l_134                  ; 14F74

		if (r2 >= 128 (80) || r2 < 96 (60, '`')) { ; 14F80
			if (r5 == 1) b .l_242
			if (r3 >= 144 (90)) goto  .l_16A
			else if (r3 >= 128) goto .l_242
			else if (r3 < 96 (60, '`')) goto .l_242;
			goto .l_16A
		}
		// ;-----------------------
	.l_0E6:
		cmp r5, 255 (ff)               ; 14F9A
		bc eq, .l_178                  ; 14F9C
		and r2, 15 (0f)                ; 14F9E
		add r1, 246 (f6)               ; 14FA0
		cmp r1, 3 (03)                 ; 14FA2
		bc eq, .l_128                  ; 14FA4
		cmp r1, 98 (62, 'b')           ; 14FA6
		bc lt, .l_140                  ; 14FA8
		bl f_14726                     ; 14FAA
		bc ne, .l_100                  ; 14FAE
		b .l_238                       ; 14FB0
	.l_100:
		bl f_1473A                     ; 14FB4
		l r5, [er12]                   ; 14FB8
		push r5                        ; 14FBA
		push er0                       ; 14FBC
		mov er0, er12                  ; 14FBE
		add er0, 20 (14)               ; 14FC0
		bl f_154F2                     ; 14FC2
		pop er0                        ; 14FC6
		l r5, [er12]                   ; 14FC8
		and r5, 240 (f0)               ; 14FCA
		or r5, r4                      ; 14FCC
		st r5, [er12]                  ; 14FCE
		pop r4                         ; 14FD0
		mov r2, r4                     ; 14FD2
		and r2, 15 (0f)                ; 14FD4
		bl f_1547E.l_010               ; 14FD6
		add r1, 165 (a5)               ; 14FDA
	.l_128:
		cmp r2, 4 (04)                 ; 14FDC
		bc lt, .l_1DE                  ; 14FDE
		mov r4, r2                     ; 14FE0
		bl f_14748                     ; 14FE2
		bc al, .l_1DE                  ; 14FE6
	.l_134:
		cmp r5, 255 (ff)               ; 14FE8
		bc eq, .l_178                  ; 14FEA
		and r2, 15 (0f)                ; 14FEC
		add r1, 245 (f5)               ; 14FEE
		bc eq, .l_128                  ; 14FF0
		add r1, 1 (01)                 ; 14FF2
	.l_140:
		cmp r2, 4 (04)                 ; 14FF4
		bc ge, .l_15E                  ; 14FF6
		bl f_14726                     ; 14FF8
		bc eq, .l_238                  ; 14FFC
		bl f_1473A                     ; 14FFE
		l r5, [er12]                   ; 15002
		mov r2, r5                     ; 15004
		and r5, 240 (f0)               ; 15006
		or r5, r4                      ; 15008
		st r5, [er12]                  ; 1500A
		mov r4, r2                     ; 1500C
		bl f_1547E.l_010               ; 1500E
	.l_15E:
		cmp r1, 85 (55, 'U')           ; 15012
		bc lt, .l_1DE                  ; 15014
		bc ne, .l_166                  ; 15016
		add r1, 11 (0b)                ; 15018
	.l_166:
		add r1, 165 (a5)               ; 1501A
		bc al, .l_1DE                  ; 1501C
	.l_16A:
		cmp r1, 45 (2d, '-')           ; 1501E
		bc ne, .l_23C                  ; 15020
		bl f_14758                     ; 15022
		mov r4, r2                     ; 15026
		mov r2, r3                     ; 15028
		mov r3, r4                     ; 1502A
	.l_178:
		cmp r1, 47 (2f, '/')           ; 1502C
		bc eq, .l_1B8                  ; 1502E
		cmp r1, 45 (2d, '-')           ; 15030
		bc ne, .l_192                  ; 15032
		cmp r3, 144 (90)               ; 15034
		bc lt, .l_188                  ; 15036
		add r1, 3 (03)                 ; 15038
		bc al, .l_192                  ; 1503A
	.l_188:
		cmp r3, 128 (80)               ; 1503C
		bc ge, .l_192                  ; 1503E
		cmp r3, 96 (60, '`')           ; 15040
		bc lt, .l_192                  ; 15042
		add r1, 4 (04)                 ; 15044
	.l_192:
		add r1, 222 (de)               ; 15046
		mov r4, r2                     ; 15048
		and r4, 15 (0f)                ; 1504A
		cmp r4, 4 (04)                 ; 1504C
		bc ge, .l_1C6                  ; 1504E
		bl f_14726                     ; 15050
		bc eq, .l_238                  ; 15054
		bl f_1473A                     ; 15056
		l r5, [er12]                   ; 1505A
		mov r2, r5                     ; 1505C
		and r5, 240 (f0)               ; 1505E
		or r5, r4                      ; 15060
		st r5, [er12]                  ; 15062
		mov r4, r2                     ; 15064
		bl f_1547E.l_010               ; 15066
		bc al, .l_1C6                  ; 1506A
	.l_1B8:
		mov r1, 13 (0d)                ; 1506C
		mov r4, r2                     ; 1506E
		and r4, 15 (0f)                ; 15070
		cmp r4, 4 (04)                 ; 15072
		bc lt, .l_1C6                  ; 15074
		bl f_14748                     ; 15076
	.l_1C6:
		cmp r3, 144 (90)               ; 1507A
		bc ge, .l_1D2                  ; 1507C
		cmp r3, 128 (80)               ; 1507E
		bc ge, .l_1DE                  ; 15080
		cmp r3, 96 (60, '`')           ; 15082
		bc lt, .l_1DE                  ; 15084

	; 15086
	.l_1D2:
		r4 = r3 & 0x0f;
		if (r4 >= 4) {
			bl f_14748; // mask out bit (r4 + 3) % 8 (0:lsb .. 7:msb) from r0
		}
	.l_1DE: ; 15092
		[d_08121] = r0
		er4 = 0x1ae6
	.l_1E6: ; 1509A
		backup (r6) {
			l r6, [d_080F9]                ; 1509C
			if (r1 >= 0x17 && r1 <= 0x1c) {
				mov r2, 0
			} else {
				er2 = er12 + 0x14
			}
			er4 = [er4 + (r1 <<= 1)]
			er0 = er12

			bl er4                         ; 150BA // ##TODO CRITICAL PART ##
			mov r1, r6                     ; 150BC
		}

	.l_20C:
		cmp r0, 0 (00)                 ; 150C0
		bc ne, .l_232                  ; 150C2
		l r2, [er12]                   ; 150C4
		and r2, 240 (f0)               ; 150C6
		cmp r1, 196 (c4)               ; 150C8
		bc ne, .l_228                  ; 150CA
		cmp r2, 128 (80)               ; 150CC
		bc eq, .l_232                  ; 150CE
		cmp r2, 64 (40, '@')           ; 150D0
		bc eq, .l_22C                  ; 150D2
		mov er0, er12                  ; 150D4
		bl f_17202                     ; 150D6
		bc al, .l_232                  ; 150DA
	.l_228:
		cmp r2, 96 (60, '`')           ; 150DC
		bc ge, .l_232                  ; 150DE
	.l_22C:
		mov er0, er12                  ; 150E0
		bl f_1B238                     ; 150E2
	.l_232:
		mov r2, r0                     ; 150E6
		b .l_01E                       ; 150E8
	.l_238:
		mov r2, 7 (07)                 ; 150EC
		pop pc                         ; 150EE

	.l_23C:
		mov r2, 3 (03)                 ; 150F0
		b .l_01E                       ; 150F2
	.l_242:
		l r0, [d_080F9]                ; 150F6
		cmp r1, 119 (77, 'w')          ; 150FA
		bc eq, .l_2A4                  ; 150FC
		cmp r1, 120 (78, 'x')          ; 150FE
		bc eq, .l_2A8                  ; 15100
		cmp r1, 118 (76, 'v')          ; 15102
		bc eq, .l_260                  ; 15104
		cmp r1, 55 (37, '7')           ; 15106
		bc lt, .l_26E                  ; 15108
		cmp r1, 116 (74, 't')          ; 1510A
		bc eq, .l_26A                  ; 1510C
		cmp r1, 95 (5f, '_')           ; 1510E
		bc ge, .l_26C                  ; 15110
		add r1, 201 (c9)               ; 15112
	.l_260:
		push r0                        ; 15114
		bl f_14D24                     ; 15116
		pop r1                         ; 1511A
		bc al, .l_20C                  ; 1511C
	.l_26A:
		add r1, 10 (0a)                ; 1511E
	.l_26C:
		add r1, 216 (d8)               ; 15120
	.l_26E:
		add r1, 253 (fd)               ; 15122
		cmp r0, 196 (c4)               ; 15124
		bc ne, .l_29E                  ; 15126
		cmp r1, 67 (43, 'C')           ; 15128
		bc ge, .l_29E                  ; 1512A
		cmp r1, 64 (40, '@')           ; 1512C
		bc ge, .l_29C                  ; 1512E
		cmp r1, 52 (34, '4')           ; 15130
		bc eq, .l_29A                  ; 15132
		cmp r1, 43 (2b, '+')           ; 15134
		bc gt, .l_29E                  ; 15136
		cmp r1, 40 (28, '(')           ; 15138
		bc ge, .l_298                  ; 1513A
		cmp r1, 20 (14)                ; 1513C
		bc eq, .l_296                  ; 1513E
		cmp r1, 9 (09)                 ; 15140
		bc eq, .l_294                  ; 15142
		cmp r1, 8 (08)                 ; 15144
		bc ne, .l_29E                  ; 15146
	.l_294:
		add r1, 10 (0a)                ; 15148
	.l_296:
		add r1, 19 (13)                ; 1514A
	.l_298:
		add r1, 8 (08)                 ; 1514C
	.l_29A:
		add r1, 11 (0b)                ; 1514E
	.l_29C:
		add r1, 16 (10)                ; 15150
	.l_29E: ; 15152
		mov er4, 0x1b06
		bc al, .l_1E6                  ; 15156
	.l_2A4:
		mov r1, 30 (1e)                ; 15158
		bc al, .l_29E                  ; 1515A
	.l_2A8:
		mov r1, 84 (54, 'T')           ; 1515C
		bc al, .l_29E                  ; 1515E
}

--------------------------------------------------------------
f_15174 ; Call above function. (f_14EB4)

// call once per expression -> suspect evaluate()

// r2 = 0: multiple entry_point.
f_15174 (byte b1 @ r2 = 0, ...) {

	mov r2, 0 (00)                 ; 15174

	push lr                        ; 1517E
	push r8                        ; 15180
	mov r8, b1                     ; 15182
	mov r2, 0 (00)                 ; 15184
	; 15186
	do {
		cmp r10, 0 (00)
		bc eq, __return                  ; 15188
		r4 = f_15228(r10 = r10);
		cmp r4, 115 (73, 's')          ; 1518E
		bc eq, .l_05E                  ; 15190
		cmp r4, 2 (02)                 ; 15192
		bc le, __return                  ; 15194
		bl f_15160                     ; 15196
		bc ge, .l_04A                  ; 1519A
		if (r8 == 0) {
			.l_04A
		} else if (r8 == 1) {
			.l_048
		}
		if (r4 < 32 (20, ' ')) {
			 .l_04A                  ; 151A4
		}
		if (r4 == 32) {
			bl f_112AA.l_012               ; 151A8
			if (r0 != 0) {
				l_04A                  ; 151AE
			}
		}
		if (r4 <= 37 (25, '%')
			||
			r4 == 119 (77, 'w')          ; 151B4
			||
			r4 == 120 (78, 'x')          ; 151B8
		) __return
	.l_048:
		or r8, 2 (02)                  ; 151BC
	.l_04A: // ; 151BE
		-- r10
		mov r1, r4                     ; 151C0
		bl f_14EB4                     ; 151C2
		if (r8 == 3) __return
	} while (r2 == 0);

	__return:
		pop r8                         ; 151CE
		pop pc                         ; 151D0
	.l_05E:
		mov r2, 2 (02)                 ; 151D2
		bc al, __return                  ; 151D4
}

--------------------------------------------------------------
f_152D8 //; may call f_14EB4, but not call while calculating
f_152D8(r10, r0, ???) {

	push lr                        ; 152D8
	while (true) {
		push r0                        ; 152DA
		if (r10 == 0) __return_0
		r4 = f_15228(r10 = r10); // implicit in function
		if (r4 == 115 (73, 's') && r0 != 115 (73, 's') {
			mov r2, 2 (02)                 ; 152EC
			bc al, __return_r2                  ; 152EE
		}
		f_152A4(r1 = r4)
		if (r4 == 0) __return_0
		if (r4 == 1) {
			if (r0 == 100 (64, 'd')) {
				__return_0
			}
		}
		-- r10
		bl f_14EB4                     ; above function
		if (r2 != 0) __return_r2
		pop r0                         ; 1530A
	}
	__return_0:
		mov r2, 0 (00)                 ; 1530E
	__return_r2:
		pop r0                         ; 15310
		pop pc                         ; 15312
}

--------------------------------------------------------------
(byte @ r4) f_15228 (byte address @ r10) {
	byte[]& btable_805f = *(byte[]*)0x805f;
	return btable_805f[address];
}

--------------------------------------------------------------

/// mask out bit (r4 + 3) % 8 (0:lsb .. 7:msb) from r0
void f_14748(byte& b1 @ r0, byte b2 @ r4) { // affect r5 and b1

	r5 = ~(0x80 >> (b2 - 4)); // note that b2 may be <4 as well, in that case
	b1 &= r5;
}

--------------------------------------------------------------

(byte @ r0) f_14A00 (byte r0, byte r6, near ptr er12) {

	if (r0 != 0 || r6 != 2) return r0;
	f_1B03E(er0 = er12, ...)
	if (r0 == 1) return 0;

	push r0                        //; 14A18
	er0 = 0x1aae
	if (1 == byte[d_080FA]) er0 += 0x0a
	er2 = er12 + 0x28;
	f_154F2.l_04A(???);
	pop r0                         //; 14A2C

	if (r0 != 4) {
		byte [er2+9] = r1 = 6
		f_1B03E.l_06A(er0 = er12, er2 = er2)
		if (r0 != 2)
			return 0;
		else
			return 3;
	}
	f_1B03E.l_06A(er0 = er12, er2 = er2);
	if (r0 != 2)
		return 3;
	else
		return 0;
}

--------------------------------------------------------------

(byte @ r0) f_1B03E.l_06A (dword xr0) {  //; 1B0A8
	dword [d_0805C] = xr0;
	byte [d_0803A] = 0;
.l_07C: //; 1B0BA
	f_19F28();
	if (
		f_18FA2.l_008()			// [d_08009] >= 0x0a
		||
		f_18FA2()				// [d_08019] >= 0x0a
	) return 0xf0;
	return f_1743C();
}

------------

# Undecoded parts.

------------



Copy registers around:

	er2 = er0, er0 += er4
	r0 = r2
	r0 = r8, pop r8
	er0 = er8
	er0 = er6, er2 = er12
	r0 = r1
	er10 = er0
	er12 = er14
	pop r0
	r2 = r1 , ++ er14
	r0 = r2 , er2 = er10, pop qr8
	er8 = er0, er10 = er2
	er6 = er0, er0 = er8, pop qr8

-------

re[?] = im[4888] : shutdown the screen. (?)
