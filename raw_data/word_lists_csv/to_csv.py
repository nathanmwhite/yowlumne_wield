#! /usr/bin/python3

import logging
import os
import re

import pandas as pd

logging.basicConfig(level=logging.DEBUG)

data = {}
for item in [file for file in os.listdir() if file[-3:] == 'int']:
	cat = item[:-4]
	with open(item, 'r+') as f:
		data[cat] = [line.strip() for line in f.readlines()]
		for i, line in enumerate(data[cat]):
			intermediate = re.sub('"', "'", line)
			intermediate = re.sub('‘', "'", intermediate)
			intermediate = re.sub('’', "'", intermediate)
			intermediate = re.sub(" '", "\t'", intermediate)
			intermediate = re.sub("' ", "'\t", intermediate)
			data[cat][i] = intermediate.split('\t')

data_df = {}
for item in data:
	data_df[item] = pd.DataFrame(data=[line for line in data[item] if len(line) == 3])
	data_df[item]['pos'] = item
	for line in [line for line in data[item] if len(line) < 3]:
		logging.debug('shorter: %s', repr(line))

df_complete = pd.concat(data_df[item] for item in data_df)

df_complete.columns = ['word', 'meaning', 'source', 'pos']

df_complete.reset_index(drop=True, inplace=True)

df_complete.to_csv('vocab.csv', sep='\t')



