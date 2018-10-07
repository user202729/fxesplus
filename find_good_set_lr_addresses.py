# Find addresses to call to set LR to a "POP PC" command with
# minimal effect on the calculator.
# This is supposed to be called only once (per ROM) to fill builtins list.

st='''
002764   01 F0 50 4E        BL      00h:04E50h
002768   8E F2              POP     PC

002778   01 F0 EA 96        BL      00h:096EAh
00277C   8E F2              POP     PC

002B0A   01 F0 7A 2E        BL      00h:02E7Ah
002B0E   8E F2              POP     PC

002B28   01 F0 7A 2E        BL      00h:02E7Ah
002B2C   8E F2              POP     PC

002BE2   01 F0 7A 2E        BL      00h:02E7Ah
002BE6   8E F2              POP     PC

002BFE   01 F0 7A 2E        BL      00h:02E7Ah
002C02   8E F2              POP     PC

002CF8   01 F0 A8 44        BL      00h:044A8h
002CFC   8E F2              POP     PC

003474   01 F0 FE 2C        BL      00h:02CFEh
003478   8E F2              POP     PC

0035B2   01 F0 2C 31        BL      00h:0312Ch
0035B6   8E F2              POP     PC

004494   01 F1 8A B4        BL      01h:0B48Ah
004498   8E F2              POP     PC

0044A2   01 F0 A8 44        BL      00h:044A8h
0044A6   8E F2              POP     PC

004722   01 F0 EA 47        BL      00h:047EAh
004726   8E F2              POP     PC

0049FC   01 F0 78 2E        BL      00h:02E78h
004A00   8E F2              POP     PC

004A0A   01 F0 9E 4C        BL      00h:04C9Eh
004A0E   8E F2              POP     PC

004CA4   01 F0 54 B6        BL      00h:0B654h
004CA8   8E F2              POP     PC

004CD6   01 F0 58 35        BL      00h:03558h
004CDA   8E F2              POP     PC

008EFA   01 F0 B6 44        BL      00h:044B6h
008EFE   8E F2              POP     PC

00A972   01 F0 78 A9        BL      00h:0A978h
00A976   8E F2              POP     PC

00ABF6   01 F0 A8 44        BL      00h:044A8h
00ABFA   8E F2              POP     PC

00AF10   01 F0 B6 44        BL      00h:044B6h
00AF14   8E F2              POP     PC

00AFDA   01 F0 98 45        BL      00h:04598h
00AFDE   8E F2              POP     PC

00B008   01 F0 B8 B8        BL      00h:0B8B8h
00B00C   8E F2              POP     PC

00B03C   01 F0 9A 44        BL      00h:0449Ah
00B040   8E F2              POP     PC

00B084   01 F0 4E B0        BL      00h:0B04Eh
00B088   8E F2              POP     PC

00C11C   01 F0 DC 58        BL      00h:058DCh
00C120   8E F2              POP     PC

010714   01 F1 3E B0        BL      01h:0B03Eh
010718   8E F2              POP     PC

010746   01 F0 4E 45        BL      00h:0454Eh
01074A   8E F2              POP     PC

0108DE   01 F1 88 B2        BL      01h:0B288h
0108E2   8E F2              POP     PC

010906   01 F1 88 B2        BL      01h:0B288h
01090A   8E F2              POP     PC

011264   01 F1 08 B2        BL      01h:0B208h
011268   8E F2              POP     PC

0112FC   01 F1 38 B2        BL      01h:0B238h
011300   8E F2              POP     PC

011398   01 F1 F6 B0        BL      01h:0B0F6h
01139C   8E F2              POP     PC

01145C   01 F1 88 B2        BL      01h:0B288h
011460   8E F2              POP     PC

011472   01 F1 8A B4        BL      01h:0B48Ah
011476   8E F2              POP     PC

011590   01 F1 88 B2        BL      01h:0B288h
011594   8E F2              POP     PC

0115FC   01 F1 88 B2        BL      01h:0B288h
011600   8E F2              POP     PC

011632   01 F1 FC A3        BL      01h:0A3FCh
011636   8E F2              POP     PC

01169E   01 F1 88 B2        BL      01h:0B288h
0116A2   8E F2              POP     PC

0117F0   01 F1 88 B2        BL      01h:0B288h
0117F4   8E F2              POP     PC

011848   01 F1 88 B2        BL      01h:0B288h
01184C   8E F2              POP     PC

0118CA   01 F1 88 B2        BL      01h:0B288h
0118CE   8E F2              POP     PC

0118FE   01 F1 02 13        BL      01h:01302h
011902   8E F2              POP     PC

011952   01 F1 14 13        BL      01h:01314h
011956   8E F2              POP     PC

0119B2   01 F1 88 B2        BL      01h:0B288h
0119B6   8E F2              POP     PC

011A5A   01 F1 88 B2        BL      01h:0B288h
011A5E   8E F2              POP     PC

011A96   01 F1 88 B2        BL      01h:0B288h
011A9A   8E F2              POP     PC

011AD8   01 F1 88 B2        BL      01h:0B288h
011ADC   8E F2              POP     PC

011B12   01 F1 88 B2        BL      01h:0B288h
011B16   8E F2              POP     PC

011B5E   01 F1 88 B2        BL      01h:0B288h
011B62   8E F2              POP     PC

011BA0   01 F1 88 B2        BL      01h:0B288h
011BA4   8E F2              POP     PC

011BF0   01 F1 88 B2        BL      01h:0B288h
011BF4   8E F2              POP     PC

011C30   01 F1 88 B2        BL      01h:0B288h
011C34   8E F2              POP     PC

011C76   01 F1 88 B2        BL      01h:0B288h
011C7A   8E F2              POP     PC

011CB4   01 F1 88 B2        BL      01h:0B288h
011CB8   8E F2              POP     PC

011CF0   01 F1 88 B2        BL      01h:0B288h
011CF4   8E F2              POP     PC

011D2C   01 F1 88 B2        BL      01h:0B288h
011D30   8E F2              POP     PC

011D66   01 F1 88 B2        BL      01h:0B288h
011D6A   8E F2              POP     PC

011DC6   01 F1 A6 21        BL      01h:021A6h
011DCA   8E F2              POP     PC

011E62   01 F1 F2 12        BL      01h:012F2h
011E66   8E F2              POP     PC

011F76   01 F1 02 13        BL      01h:01302h
011F7A   8E F2              POP     PC

011FA6   01 F1 14 13        BL      01h:01314h
011FAA   8E F2              POP     PC

011FDE   01 F1 02 13        BL      01h:01302h
011FE2   8E F2              POP     PC

01200E   01 F1 14 13        BL      01h:01314h
012012   8E F2              POP     PC

012046   01 F1 02 13        BL      01h:01302h
01204A   8E F2              POP     PC

012076   01 F1 14 13        BL      01h:01314h
01207A   8E F2              POP     PC

0120AE   01 F1 02 13        BL      01h:01302h
0120B2   8E F2              POP     PC

0120DE   01 F1 14 13        BL      01h:01314h
0120E2   8E F2              POP     PC

012116   01 F1 02 13        BL      01h:01302h
01211A   8E F2              POP     PC

012146   01 F1 14 13        BL      01h:01314h
01214A   8E F2              POP     PC

0121A0   01 F1 88 B2        BL      01h:0B288h
0121A4   8E F2              POP     PC

0122C8   01 F1 88 B2        BL      01h:0B288h
0122CC   8E F2              POP     PC

012324   01 F1 88 B2        BL      01h:0B288h
012328   8E F2              POP     PC

0123DC   01 F1 88 B2        BL      01h:0B288h
0123E0   8E F2              POP     PC

012546   01 F1 88 B2        BL      01h:0B288h
01254A   8E F2              POP     PC

012830   01 F1 88 B2        BL      01h:0B288h
012834   8E F2              POP     PC

012932   01 F1 88 B2        BL      01h:0B288h
012936   8E F2              POP     PC

012A26   01 F1 88 B2        BL      01h:0B288h
012A2A   8E F2              POP     PC

0133DC   01 F1 28 AA        BL      01h:0AA28h
0133E0   8E F2              POP     PC

0133F4   01 F1 8A B4        BL      01h:0B48Ah
0133F8   8E F2              POP     PC

0138CE   01 F1 B8 B1        BL      01h:0B1B8h
0138D2   8E F2              POP     PC

0139A8   01 F1 B4 3B        BL      01h:03BB4h
0139AC   8E F2              POP     PC

0139DE   01 F1 EC A9        BL      01h:0A9ECh
0139E2   8E F2              POP     PC

013B3C   01 F0 A8 44        BL      00h:044A8h
013B40   8E F2              POP     PC

014166   01 F1 D4 3B        BL      01h:03BD4h
01416A   8E F2              POP     PC

014188   01 F1 4A 72        BL      01h:0724Ah
01418C   8E F2              POP     PC

0141D4   01 F1 EC A9        BL      01h:0A9ECh
0141D8   8E F2              POP     PC

0143BC   01 F1 00 AA        BL      01h:0AA00h
0143C0   8E F2              POP     PC

014446   01 F1 C6 34        BL      01h:034C6h
01444A   8E F2              POP     PC

014862   01 F1 D8 AF        BL      01h:0AFD8h
014866   8E F2              POP     PC

0148AE   01 F1 4C A4        BL      01h:0A44Ch
0148B2   8E F2              POP     PC

0148C6   01 F1 3C 48        BL      01h:0483Ch
0148CA   8E F2              POP     PC

0148DA   01 F1 B8 B1        BL      01h:0B1B8h
0148DE   8E F2              POP     PC

014AA2   01 F1 86 71        BL      01h:07186h
014AA6   8E F2              POP     PC

014AAC   01 F1 42 11        BL      01h:01142h
014AB0   8E F2              POP     PC

014AB8   01 F1 00 4A        BL      01h:04A00h
014ABC   8E F2              POP     PC

014AC4   01 F1 00 4A        BL      01h:04A00h
014AC8   8E F2              POP     PC

014AD0   01 F1 00 4A        BL      01h:04A00h
014AD4   8E F2              POP     PC

014AE6   01 F1 88 B3        BL      01h:0B388h
014AEA   8E F2              POP     PC

014B10   01 F1 8E 6D        BL      01h:06D8Eh
014B14   8E F2              POP     PC

014B16   01 F1 10 71        BL      01h:07110h
014B1A   8E F2              POP     PC

014B24   01 F1 00 AA        BL      01h:0AA00h
014B28   8E F2              POP     PC

014B2A   01 F1 E2 6E        BL      01h:06EE2h
014B2E   8E F2              POP     PC

014B38   01 F1 EC A9        BL      01h:0A9ECh
014B3C   8E F2              POP     PC

014B3E   01 F1 3A 6F        BL      01h:06F3Ah
014B42   8E F2              POP     PC

014B4C   01 F1 28 AA        BL      01h:0AA28h
014B50   8E F2              POP     PC

014BA2   01 F1 A2 6E        BL      01h:06EA2h
014BA6   8E F2              POP     PC

014BB0   01 F1 14 AA        BL      01h:0AA14h
014BB4   8E F2              POP     PC

014BB6   01 F1 5E 6F        BL      01h:06F5Eh
014BBA   8E F2              POP     PC

014D0C   01 F1 14 AA        BL      01h:0AA14h
014D10   8E F2              POP     PC

014D1E   01 F1 44 A7        BL      01h:0A744h
014D22   8E F2              POP     PC

014D6A   01 F1 38 B2        BL      01h:0B238h
014D6E   8E F2              POP     PC

014ED2   01 F1 96 55        BL      01h:05596h
014ED6   8E F2              POP     PC

01565C   01 F1 96 55        BL      01h:05596h
015660   8E F2              POP     PC

01570C   01 F1 5A 53        BL      01h:0535Ah
015710   8E F2              POP     PC

01574C   01 F1 82 56        BL      01h:05682h
015750   8E F2              POP     PC

0158E4   01 F1 5A 53        BL      01h:0535Ah
0158E8   8E F2              POP     PC

0160FA   01 F1 0E 9C        BL      01h:09C0Eh
0160FE   8E F2              POP     PC

016640   01 F1 B8 B1        BL      01h:0B1B8h
016644   8E F2              POP     PC

016660   01 F1 8A B4        BL      01h:0B48Ah
016664   8E F2              POP     PC

01691A   01 F1 3E 68        BL      01h:0683Eh
01691E   8E F2              POP     PC

016932   01 F1 B8 68        BL      01h:068B8h
016936   8E F2              POP     PC

01699A   01 F1 24 62        BL      01h:06224h
01699E   8E F2              POP     PC

0169F6   01 F1 6E 67        BL      01h:0676Eh
0169FA   8E F2              POP     PC

016A1E   01 F1 C2 67        BL      01h:067C2h
016A22   8E F2              POP     PC

016BD8   01 F1 00 61        BL      01h:06100h
016BDC   8E F2              POP     PC

016BF0   01 F1 38 A4        BL      01h:0A438h
016BF4   8E F2              POP     PC

016C2E   01 F1 00 61        BL      01h:06100h
016C32   8E F2              POP     PC

016C4E   01 F1 4C A4        BL      01h:0A44Ch
016C52   8E F2              POP     PC

0170CA   01 F1 F6 B0        BL      01h:0B0F6h
0170CE   8E F2              POP     PC

0170EA   01 F1 28 AA        BL      01h:0AA28h
0170EE   8E F2              POP     PC

01710A   01 F1 28 AA        BL      01h:0AA28h
01710E   8E F2              POP     PC

017180   01 F1 A2 6E        BL      01h:06EA2h
017184   8E F2              POP     PC

0172C6   01 F1 F2 78        BL      01h:078F2h
0172CA   8E F2              POP     PC

01738A   01 F1 3C A2        BL      01h:0A23Ch
01738E   8E F2              POP     PC

0174F6   01 F1 92 A0        BL      01h:0A092h
0174FA   8E F2              POP     PC

01751E   01 F1 E6 A3        BL      01h:0A3E6h
017522   8E F2              POP     PC

017620   01 F1 BA A0        BL      01h:0A0BAh
017624   8E F2              POP     PC

017684   01 F1 0E 9C        BL      01h:09C0Eh
017688   8E F2              POP     PC

0176AE   01 F1 98 78        BL      01h:07898h
0176B2   8E F2              POP     PC

017764   01 F1 E6 A3        BL      01h:0A3E6h
017768   8E F2              POP     PC

017820   01 F1 D6 9B        BL      01h:09BD6h
017824   8E F2              POP     PC

017986   01 F1 56 7D        BL      01h:07D56h
01798A   8E F2              POP     PC

017AD8   01 F1 56 79        BL      01h:07956h
017ADC   8E F2              POP     PC

017B54   01 F1 0E 9C        BL      01h:09C0Eh
017B58   8E F2              POP     PC

017BB4   01 F1 F4 7B        BL      01h:07BF4h
017BB8   8E F2              POP     PC

017DBE   01 F1 58 9D        BL      01h:09D58h
017DC2   8E F2              POP     PC

017E20   01 F1 46 8B        BL      01h:08B46h
017E24   8E F2              POP     PC

01806E   01 F1 E6 A3        BL      01h:0A3E6h
018072   8E F2              POP     PC

0181D4   01 F1 3C A2        BL      01h:0A23Ch
0181D8   8E F2              POP     PC

0182D6   01 F1 0E 9C        BL      01h:09C0Eh
0182DA   8E F2              POP     PC

0183A4   01 F1 E6 A3        BL      01h:0A3E6h
0183A8   8E F2              POP     PC

01855C   01 F1 88 8C        BL      01h:08C88h
018560   8E F2              POP     PC

018570   01 F1 58 9D        BL      01h:09D58h
018574   8E F2              POP     PC

018AA0   01 F1 3C A2        BL      01h:0A23Ch
018AA4   8E F2              POP     PC

018B22   01 F1 D6 73        BL      01h:073D6h
018B26   8E F2              POP     PC

018B8A   01 F1 3C A2        BL      01h:0A23Ch
018B8E   8E F2              POP     PC

018C9A   01 F1 F2 78        BL      01h:078F2h
018C9E   8E F2              POP     PC

018F28   01 F1 E6 A3        BL      01h:0A3E6h
018F2C   8E F2              POP     PC

018F6E   01 F1 3C A2        BL      01h:0A23Ch
018F72   8E F2              POP     PC

019040   01 F1 E6 A3        BL      01h:0A3E6h
019044   8E F2              POP     PC

019106   01 F1 F4 9B        BL      01h:09BF4h
01910A   8E F2              POP     PC

019402   01 F1 3C A2        BL      01h:0A23Ch
019406   8E F2              POP     PC

019814   01 F1 3C A2        BL      01h:0A23Ch
019818   8E F2              POP     PC

019BE8   01 F1 F2 78        BL      01h:078F2h
019BEC   8E F2              POP     PC

019C06   01 F1 F2 78        BL      01h:078F2h
019C0A   8E F2              POP     PC

019C20   01 F1 F2 78        BL      01h:078F2h
019C24   8E F2              POP     PC

019D18   01 F1 E6 A3        BL      01h:0A3E6h
019D1C   8E F2              POP     PC

019D4E   01 F1 F2 78        BL      01h:078F2h
019D52   8E F2              POP     PC

019D6A   01 F1 F2 78        BL      01h:078F2h
019D6E   8E F2              POP     PC

019ECA   01 F1 3C A2        BL      01h:0A23Ch
019ECE   8E F2              POP     PC

019FB8   01 F1 F2 78        BL      01h:078F2h
019FBC   8E F2              POP     PC

01A02E   01 F1 F2 78        BL      01h:078F2h
01A032   8E F2              POP     PC

01A056   01 F1 F2 78        BL      01h:078F2h
01A05A   8E F2              POP     PC

01A084   01 F1 F2 78        BL      01h:078F2h
01A088   8E F2              POP     PC

01A0A4   01 F1 F2 78        BL      01h:078F2h
01A0A8   8E F2              POP     PC

01A0CC   01 F1 F2 78        BL      01h:078F2h
01A0D0   8E F2              POP     PC

01A1D0   01 F1 3C A2        BL      01h:0A23Ch
01A1D4   8E F2              POP     PC
'''[1:-1]

import re

adrs=[re.sub(r'.*BL *(.*)h:0(.*)h\n.*',r'\1\2',x) for x in st.split('\n\n')]
adrs=list(set(adrs))

file=open('/home/user202729/fxesp/disas_real_570es+.txt','r')
code=file.read()
file.close()

for adr in adrs:
	i=code.index(adr)
	if code[i+28:i+38]=='PUSH    LR':
		continue
	part=code[i:i+200]
	if 'RT' not in part:
		continue
	print(part)
	print()

