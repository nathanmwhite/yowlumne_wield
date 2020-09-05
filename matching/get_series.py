# THIS FILE IS DEPRECATED!!!
# Make changes to WordSeries.py!!!

import sys

def get_symbols():
	'''instantiate dictionarty of symbol_series'''
	filename = "symbol_series.txt"
	symbol_dict = {}
	with open(filename, 'r') as f:
		for line in f.readlines():
			data = line.strip().split(' ')
			for item in data:
				symbol_dict[item] = data[0]
	return symbol_dict

def get_word_series(word, symbol_dict):
	'''determines the series of each sound in word'''
	word_series = []
	current_state = ''
	for letter in word:
		if current_state == '':
			current_state = letter
			continue
		if current_state + letter in \
			[key[:len(current_state+letter)] for key in symbol_dict.keys()]:
			current_state += letter
		else:
			word_series.append(symbol_dict[current_state])
			current_state = letter
	word_series.append(symbol_dict[current_state])
	return word_series

def test_set():
	test_words = ['mani', 'waḵi', "'amnōkun", "'anūnkīn", "k`amits", "pṓtr'mō", "'ama'", "uʃ", "p`ak̄'āthinhin"]
	symbol_dict = get_symbols()
	print(symbol_dict)
	for word in test_words:
		print(word, ':', get_word_series(word, symbol_dict))

if __name__ == '__main__':
	test_set()
