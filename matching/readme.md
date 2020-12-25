Folder: ~/matching

This folder contains the files to find the best match in ~/raw_data/word_lists_csv/vocab.csv for a given word based on Levenshtein Distance.

This folder contains one subfolder:
1. Tests : test scripts using Python's unittest module

This folder contains the following code files:
1. __init__.py : empty init file that enables recognition of the "matching" folder as a module
2. df_series.py : prepares DataFrame from vocab.csv by adding a 'series' column populated by WordSeries.py
	prepare_df(df) : takes DataFrame as input and returns DataFrame with 'series'
3. get_series.py : contains an early version of WordSeries.py (deprecated)
4. levenshtein.py : contains the code for Levenshtein Distance (from stackabuse.com post)
	levenshtein(seq1, seq2) : takes two sequences and returns the Levenshtein Distance calculation
5. matcher.py : code that checks word against DataFrame and return closest match (or matches if necessary)
6. process_text.py : contains a script that preprocesses text at a basic level
7. WordSeries.py : contains WordSeries object code that enables identification of series
	WordSeries.get_series(word) : takes the input word and returns list containing series sequence

Other files:
6) notes.txt : miscellaneous notes on series and implementation (deprecated)
7) sample.txt : sample text for testing
8) symbol_series.txt : text file containing series sequences: each series is one line, each possible element within one line is separated by spaces
