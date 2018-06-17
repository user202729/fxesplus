@:: compile
@del main.asm main.prn main.obj main.ler 2> NUL
@call init

ccu8 /TM610901 /ML /Ot /LE /SS512 main.c
@:: ML: Memory Large, Ot: optimize time, LE: Generate .LER file, SS: stack size,
@:: (I'm not sure if 512 bytes (0x200) is correct)

rasu8 /NPL main.asm

