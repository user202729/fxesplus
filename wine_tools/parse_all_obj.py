#!/usr/bin/python3
FOLDER_PATH = 'obj/'

import sys
sys.path.append('..')
from parse_obj import parse_data
import os

for file in os.listdir(os.fsencode(FOLDER_PATH)):
	filename = os.fsdecode(file)
	with open(FOLDER_PATH + filename, 'rb') as obj_file:
		data = parse_data(obj_file.read(), print = print)
	for obj_id in data['nameof_export'].keys():
		if data['typeof_export'][obj_id] == 'fn':
			print(f'Fn {data["nameof_export"][obj_id]}, '+
				f'len {len(data["obj_data"][obj_id])}')

