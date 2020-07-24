#!/bin/python3
"""
Used (with main tmp binary patch) on a problem with step in [2... 3].
Requires line format "time data confidence" -- the lower the confidence the better.
"""


import sys, argparse, subprocess, shlex

parser=argparse.ArgumentParser()
parser.add_argument("-o", "--output", action="store_true", help="Not pipe self to `less`")
parser.add_argument("input", nargs="?", help="Input file", default="/tmp/out_segment2_part4_smart_time-binarize")
parser.add_argument("--first-start", type=int, default=4)
args=parser.parse_args()

if not args.output:
	subprocess.call(' '.join(shlex.quote(argument) for argument in sys.argv)
			+" -o 2>&1 |less", shell=True)
	sys.exit(0)

with open(args.input, "r") as f:
	times, lines, confidence=zip(*(x.split() for x in f.readlines()[:-40]))

times=[*map(int, times)]
confidence=[round(float(x), 4) for x in confidence]

firststart=args.first_start
i=firststart
outputIndex=0
while True:
	warn=""
	if confidence[i]!=min(confidence[i-1:i+2]):
		warn=f"({lines[i-1]} {confidence[i-1]}), ({lines[i+1]} {confidence[i+1]})"

	print(f"{lines[i]} {confidence[i]} {i} {outputIndex and (i-firststart)/outputIndex:.5g} {warn}")
	outputIndex+=1
	_, i=min((confidence[j], j) for j in range(i+2, i+4))
