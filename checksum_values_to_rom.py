#!/bin/python
import sys, argparse

auto_int=lambda x: int(x, 0)
parser=argparse.ArgumentParser()
parser.add_argument("input", nargs="?", help="Input file", default="/tmp/f2")
parser.add_argument("output", nargs="?", help="Output binary file name", default="/tmp/out.bin")
parser.add_argument("-s", "--start-address", default=0xfe31,
		help="Start checksum address. If this is wrong, the output will be rotated",
		type=auto_int)
parser.add_argument("-c", "--chunk-size-words", default=0x01fe//2, type=auto_int)
parser.add_argument("--subtract-value", default=0x0000, type=auto_int)
parser.add_argument("-r", "--post-rotate", default=0,
		help="Number of words to rotate the result (handled after first word computation)",
		type=auto_int)
#parser.add_argument("--post-add-value", default=0x0000, type=auto_int) # use -f instead
parser.add_argument("-i", "--increment-value", help="Jump between two consecutive checksum values",
		default=0x3432, type=auto_int)
parser.add_argument("-f", "--first-word", help="First word in the output before post-rotate. "
		"Use -1 to calculate (requires subtract value to be correct)",
		default=0x0000, type=auto_int)
args=parser.parse_args()

def softset(arr,index,val):
	if arr[index] in (None,val):
		arr[index]=val
	else:
		sys.stderr.write(f'Warning: softset index: {index:04x} existing: {arr[index]:04x} new: {val:04x}\n')


with open(args.input, "r") as f:
	d=[int(x,16) for x in f.read().strip().split('\n')]
print(hex(len(d)))
a=[None]*0x8000
i=args.start_address
for x in d:
	softset(a,i//2,(args.subtract_value-x)&0xffff)
	i=(i+args.increment_value )&0xffff

# print('\n'.join(f'= {i:04x}' if i!=None else 'None' for i in a))
# raise 1

l=args.chunk_size_words
assert l<0x8000
assert l%2!=0
# a[i]: sum of l words from address i*2

r=[None]*0x8000
i=0

assert None not in a

def inv(x,y): # inefficient
	return next(a for a in range(y) if a*x%y==1)


# compute r[0]

r[0]=args.first_word
if r[0]==-1:
	sumall=(sum(a)*inv(l,0x8000))&0xffff
	i=0
	s=0
	while (i&0x7fff)!=1:
		s+=a[i&0x7fff]
		i+=l
	# now s is the sum of i first elements
	r[0]=(s-sumall*(i>>15))&0xffff


i=0
for _ in range(0x8001):
	ipl=(i+l)&0x7fff
	si1,si=a[(i+1)&0x7fff],a[i]
	softset(r,ipl,(r[i]+si1-si)&0xffff)
	i=ipl


'''
r[0x3e6a//2:0x3e6a//2+5]=[0xf8ce,0xf46e,0xf87e,0xae1a,0xe1f0]

for _ in range(30):
	for i in [*range(0x8000),*reversed(range(0x8000))]:
		si1,si=a[(i+1)&0x7fff],a[i]
		if si!=None and si1!=None:
			ipl=(i+l)&0x7fff
			if r[i]!=None:
				softset(r,ipl,(r[i]+si1-si)&0xffff)
			if r[(i+l)&0x7fff]!=None:
				softset(r,i,(r[ipl]+si-si1)&0xffff)
'''

assert args.post_rotate>=0 and args.post_rotate<=len(r)
r=r[args.post_rotate:]+r[:args.post_rotate]

#r=[(x+args.post_add_value)&0xffff for x in r]

if 0: #print some debug information
	print('\n'.join(
		(f'= {i:04x}' if i!=None else 'None')
		+'\t'+
		(f'= {j:04x}' if j!=None else 'None')
		for i,j in zip(a,r)))

with open(args.output,'wb') as f:
	f.write(bytes(y for x in r for y in (x&0xff,x>>8)))
