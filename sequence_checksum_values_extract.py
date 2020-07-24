#!/bin/python3
"""
Used for extracting the ROM from classwiz calculators.
"""

import sys, os, itertools, argparse, subprocess, shlex

parser=argparse.ArgumentParser()
parser.add_argument("-o", "--output", action="store_true", help="Not pipe self to `less`")
parser.add_argument("--ugly-hack", action="store_true", help="Shorten consecutive runs of Fs if followed by E")
parser.add_argument("--plot-confidence", action="store_true")
parser.add_argument("input", nargs="?", help="Input file", default="/tmp/segment1_part2_1")
parser.add_argument("--num-previous-candidate", "-np", help="Number of previous candidates", default=3, type=int)
parser.add_argument("--num-next-candidate", "-nn", help="Number of next candidates", default=3, type=int)
parser.add_argument("--step", "-s", help="Step (seconds)", default=0.3745, type=float)
parser.add_argument("--step-correction", "-sc", help="Maximum error in step (seconds)", default=0.002, type=float)
parser.add_argument("--first-start", "-f", help="First start (seconds)", default=None, type=float)
parser.add_argument("--first-start-frame", "-ff", help="First start (frame)", default=None, type=float)
args=parser.parse_args()

assert args.num_previous_candidate>=0
assert args.num_next_candidate>=0

if not args.output:
	subprocess.call(' '.join(shlex.quote(argument) for argument in sys.argv)
			+" -o 2>&1 |less", shell=True)
	sys.exit(0)

with open(args.input, "r") as f:
	data=[line.split() for line in f.readlines()]
	times=[int(it[0])/1e9 for it in data]
	lines=[it[1] for it in data]
	if args.plot_confidence:
		import pyqtgraph
		confidence=[float(it[2]) for it in data]
		pyqtgraph.plot(confidence)
		input()
		sys.exit(0)

	del data #dynamic variables isn't good...

from typing import Tuple

def ugly_hack_fix_lines(lines):
	print("Applying ugly lack to manually fix lines...")

	def process1(x: Tuple[str]):
		assert type(x)==tuple
		x=list(x)
		assert all(len(a)==1 for a in x)

		for i in range(len(x)-2):
			if x[i]=="F" and x[i+1]=="E" and x[i+2]=="E":
				x[i]="E"

		return x

	lines=list(zip(*lines))
	lines=[process1(a) for a in lines]
	lines=list(zip(*lines))
	lines=["".join(a) for a in lines]

	return lines
if args.ugly_hack:
	lines=ugly_hack_fix_lines(lines)


def warn_short_runs(lines):
	for line in lines:
		assert len(line)==4, line
	for index in range(4):
		col=[line[index] for line in lines]
		groups=[list(items) for char, items in
				itertools.groupby(enumerate(col), key=lambda it: it[1])
				][1:-1]
		for items in groups:
			l=len(items)
			if l<=2:
				print(f"{index=} {items=} {l} -- too short")

#warn_short_runs(lines)

def ensure_constant_fps(times):  #usually fails...
	delta=times[1]-times[0]
	for last, cur in zip(times, times[1:]):
		assert abs((cur-last)-delta)<=10, (cur, last, cur-last, delta)

assert times==sorted(times)

#delta=times[10]-times[9]
assert (args.first_start_frame is None)!=(args.first_start is None)
if args.first_start is not None:
	firststart=args.first_start
else:
	assert args.first_start_frame is not None
	i=int(args.first_start_frame)
	if args.first_start_frame==i:
		firststart=times[i]
	else:
		firststart=times[i]*(i+1-args.first_start_frame)+times[i+1]*(args.first_start_frame-i)


#step=5*delta
#change=1.5*delta



step=args.step
change=args.step_correction

start=firststart
print(step)
#maximum abs(real step - step)

outputIndex=0

inputIndex=0

def changeInputIndex(start): #might throw IndexError
	global inputIndex
	assert times[inputIndex]<=start
	while times[inputIndex+1]<=start:
		inputIndex+=1 #might crash

warnIndex=0

minEstimatedStep=1e9
maxEstimatedStep=-1e9

while True:
	start+=step
	try:
		changeInputIndex(start)
	except IndexError:
		print(f"Estimated step: {minEstimatedStep:.5g} {maxEstimatedStep:.5g}")
		break

	value=lines[inputIndex]
	first=inputIndex
	while lines[first-1]==value: first-=1
	last=inputIndex
	while last<len(lines) and lines[last]==value: last+=1

	if last!=len(lines):
		start=max(start-change, min(start+change, (times[first]+times[last])/2))


	candidates=lines[inputIndex-args.num_previous_candidate:inputIndex+args.num_next_candidate+1]
	count=candidates.count(value)

	outputIndex+=1
	estimatedStep=(start-firststart)/outputIndex

	if outputIndex>=100:
		minEstimatedStep=min(minEstimatedStep, estimatedStep)
		maxEstimatedStep=max(maxEstimatedStep, estimatedStep)

	warn="" #on not winning
	if count*2<=len(candidates):
		warnIndex+=1
		warn=f"!!{warnIndex}: {candidates}"

	print(
			value,
			f"{count}/{len(candidates)}", #winning status
			f"nframe={last-first}",

			#f"{start-times[first]:.4g}||{times[last]-start:.4g}", #delta time
			f"{inputIndex-first:.6g}||{last-inputIndex:.6g}", #delta frame

			warn,
			f"{outputIndex} ~ {estimatedStep:.5g} ~ {inputIndex+1}",
			)
