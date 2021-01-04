#!/usr/bin/python

import os
import random
import re

def prepare_texts(source_dir, num_total_texts):
	texts = {}
	for i in range(1, num_total_texts + 1):
		# step 1: get all texts loaded
		f = open(os.path.join(source_dir, 'text ' + str(i) + ' preprocess.txt'), 'r')
		lines = f.readlines()
		# step 2: get only the words in each text
		split_lines = [l.split('\t')[0] for l in lines]
		# step 3: get only the characters in the words
		chars = ' '.join(split_lines)
		# & indicates that the following original space should not be there
		chars = re.sub('& ', ' ', chars)
		# % indicates that a proper space is missing
		chars = re.sub('% ', '', chars)
		#   the characters decide the total count of 80/20
		texts[i] = chars
	# step 4: randomly select out texts until an 80/20 combination is achieved
	# do this by allowing a band of 1% on either side
	test_portion = 0.2
	total_char_len = sum([len(t) for t in texts.values()])
	print('total character length :', total_char_len)
	max_bound = total_char_len * (test_portion + 0.01)
	min_bound = total_char_len * (test_portion - 0.01)
	return texts, max_bound, min_bound

def find_test_set(input_texts, max_bound, min_bound):
	# need to repeatedly do until a successful value is found
	current_value = 0.0
	text_numbers = []
	while True:
		# step 1: get a random integer value representing a text
		# while loop to prevent duplicate texts
		while True:
			i = random.randint(1, 20)
			if i not in text_numbers:
			    break
		text_char_length = len(texts[i])
		# step 2: add to current_value
		current_value += text_char_length
		text_numbers.append(i)
		# step 3: check current_value: is it above minimum bound?
		#   yes: is it below maximum bound?
		#    yes: return the text numbers
		#    no: start over
		#   no: do steps 1-3 again
		if current_value >= min_bound:
			if current_value <= max_bound:
			    return text_numbers
			else:
				return find_test_set(input_texts, max_bound, min_bound)
		else:
		    continue
		    
if __name__ == '__main__':
    source_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'processed_data')
    texts, max_bound, min_bound = prepare_texts(source_directory, 20)
    text_numbers = find_test_set(texts, max_bound, min_bound)
    print('text numbers:', text_numbers)
    total_test_len = sum([len(texts[i]) for i in text_numbers])
    print('total test length:', total_test_len)
    # the output on the run was texts 1, 4, 12, 17, 18; 13708/67835 characters (20.21%)
