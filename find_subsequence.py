#!/bin/python3
"""
Find shortest substrings of the ROM that matches some subsequence pattern.
Usage: edit pattern (|: might not be consecutive, space: must be consecutive bytes), edit rom_path, run.
Note: byte strings displayed are truncated to first <=25 bytes.
"""

rom_path="991cnx_emu/rom.bin"
pattern="55 94 57 98 94"

rom=open(rom_path, "rb").read()
pattern=[bytes(int(byte, 16) for byte in chunk.split()) for chunk in pattern.split("|")]

def compute():
	i=0
	segments=[]
	while True:
		pos=i
		for chunk in pattern:
			l=len(chunk)
			while True:
				if pos+l>len(rom): return segments
				if rom[pos:pos+l]==chunk: break
				pos+=1
			pos+=l

		# now [i:pos] matches pattern
		# find maximum i such that it still holds

		j=pos
		for chunk in reversed(pattern):
			l=len(chunk)
			j-=l
			while rom[j:j+l]!=chunk: j-=1
		assert j>=i

		segments.append((j, pos))
		i=j+1


segments=compute()
segments.sort(key=lambda x: x[1]-x[0])
for first, last in segments:
	print(f"{first:05x} -> {last:05x} | len={last-first:5x} | "+
			' '.join(f"{byte:02x}" for byte in rom[first:min(first+25, last)])
	)
