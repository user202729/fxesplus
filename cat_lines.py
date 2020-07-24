#!/bin/python3
import argparse, itertools, sys
parser=argparse.ArgumentParser()
parser.add_argument("files", nargs="+", type=str, help="List of files")
args=parser.parse_args()

lines=open(args.files[0]).read().strip().split('\n')
for f in args.files[1:]:
	lines1=open(f).read().strip().split('\n')
	for i in range(max(0, len(lines)-len(lines1)), len(lines)):
		if all(a==b for a, b in zip(itertools.islice(lines, i, None), lines1)):
			break
	else:
		print(f"File {f} does not have any matching line with the previous file -- error out", file=sys.stderr)
		sys.exit(1)

	assert lines[i:]==lines1[:len(lines)-i]
	print(f"File {f} has {len(lines)-i} lines in common with the previous file", file=sys.stderr)
	lines.extend(lines1[len(lines)-i:])

print(end="\n".join(lines))
