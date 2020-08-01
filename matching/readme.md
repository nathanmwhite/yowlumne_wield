Folder: ~/matching

This folder contains the files to find the best match in ~/raw_data/word_lists_csv/vocab.csv for a given word based on Levenshtein Distance.

This folder contains the following code files:
1) df_series.py : prepares DataFrame from vocab.csv by adding a 'series' column populated by WordSeries.py
	prepare_df(df) : takes DataFrame as input and returns DataFrame with 'series'
2) get_series.py : contains an early version of WordSeries.py (deprecated)
3) levenshtein.py : contains the code for Levenshtein Distance (from stackabuse.com post)
	levenshtein(seq1, seq2) : takes two sequences and returns the Levenshtein Distance calculation
4) matcher.py : will contain code to check word against DataFrame and return closest match (or matches if necessary)
	TODO: remember to include support for e/i and o/u series
5) WordSeries.py : contains WordSeries object code that enables identification of series
	WordSeries.get_series(word) : takes the input word and returns list containing series sequence

Other files:
6) notes.txt : miscellaneous notes on series and implementation (deprecated)
7) sample.txt : sample text for testing
8) symbol_series.txt : text file containing series sequences: each series is one line, each possible element within one line is separated by spaces
