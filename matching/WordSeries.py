#! /usr/bin/python3

import sys

import logging

logging.basicConfig(level=logging.DEBUG)

class WordSeries:
    def __init__(self):
        self.populate_symbols()

    def populate_symbols(self):
        '''instantiate dictionary of symbol_series'''
        filename = "symbol_series.txt"
        self._symbol_dict = {}
        with open(filename, 'r') as f:
            for line in f.readlines():
                data = line.strip().split(' ')
                for item in data:
                    self._symbol_dict[item] = data[0]

    def get_series(self, word):
        '''determines the series of each sound in word'''
        word_series = []
        current_state = ''
        for letter in word:
            if letter in ['̄', '́', '̥', '|', '̯']:
                continue
            if current_state == '':
                current_state = letter
                continue
            if current_state + letter in \
                [key[:len(current_state+letter)] for key in self._symbol_dict.keys()]:
                current_state += letter
            else:
                try:
                    logging.debug('appending: ' + str(current_state))
                    word_series.append(self._symbol_dict[current_state])
                except KeyError:
                    logging.debug('failed state: ' + str(word))
                    if current_state == '`':
                        word_series.append(self._symbol_dict["'"])
                    elif current_state == 'ʌ':
                        word_series.append(self._symbol_dict["o"])
                    else:
                        raise                
                current_state = letter
        word_series.append(self._symbol_dict[current_state])
        return word_series
