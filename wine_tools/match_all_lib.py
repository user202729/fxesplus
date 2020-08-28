#!/bin/python3
"""
Parses all .lib files in ".", match the function code against "../rom.bin".
(hard coded as default parameter in parse_all_obj.py)
"""
import os
import subprocess

for name in os.listdir("."):
	if name.lower().endswith(".lib"):
		print("Lib file name: ", name)
		subprocess.call(("python", "extract.py", name))
		subprocess.call("python parse_all_obj.py".split())
