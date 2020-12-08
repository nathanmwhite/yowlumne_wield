import logging
import re
import string
import sys
import warnings

import pandas as pd

import df_series
import process_text
import levenshtein
import WordSeries

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.DEBUG)

def try_levenshtein(word, matched):
    ws = WordSeries.WordSeries()
    a = ws.get_series(word)
    b = ws.get_series(matched)
    out = levenshtein.levenshtein(a, b)
    print(a, b, out)

def test_cases():
    try_levenshtein('waki', 'wakiy')
    try_levenshtein('hiyuk', 'hiyuk')
    try_levenshtein('hoho', 'hǫ:hǫ')
    try_levenshtein('pānahin', 'pana')
    try_levenshtein('pokhin', "bok'o")

class Matcher:
    def __init__(self):
        temp_df = pd.read_csv('../raw_data/word_lists_csv/vocab.csv',
                     sep='\t',
                     index_col=0,
                     keep_default_na=False,
                     na_values=['_'])
        self.df = df_series.prepare_df(temp_df)

    def quick_stem(self, word):
        if word[-3:] in ['hin', 'hun'] and len(word) > 5:
            return word[:-3]
        elif word[-3:] in ["xo'", "qo'"] and len(word) > 5:
            return word[:-3]
        elif word[-2:] in ["xo", "qo"] and len(word) > 5:
            return word[:-2]
        else:
            return word

    def file_prep(self, filename):
        f = open('../raw_data/training_text/' + filename, 'r')
        lines = f.readlines()
        f.close()
        data = ' '.join(l.strip() for l in lines[2:])
        data = re.sub('-', '', data)
        data = re.sub('\.', ' . ', data)
        data = re.sub(',', ' , ', data)
        data = re.sub('\(', '( ', data)
        data = re.sub('\)', ' )', data)
        data = re.sub('=', ' = ', data)
        data = re.sub('!', ' !', data)
#        data = re.sub(':', ' : ', data) # this is possible because Harrington doesn't use : for length; it fails for Newman
        data = re.sub(':', '', data)
        data = re.sub(';', ' ; ', data)
        data = re.sub('  ', ' ', data)
        data = re.sub('  ', ' ', data)
        data = re.sub('#', '', data)
        data = re.sub('^', '', data)
        data = re.sub('\?', ' ?', data)
        data = re.sub('"', ' " ', data)
        return data.split(' ')

    # this could form the basis of a parser
    # note: need to go from larger ending to smaller ending
    def quick_stem_series(self, w):
        word = ''.join(w)
        # verbs
        if word[-5:] in ["xohin"] and len(word) > 7:
            return w[:-5]
        elif word[-3:] in ['hin', 'hun'] and len(word) > 5:
            return w[:-3]
        elif word[-3:] in ['eni'] and len(word) > 5:
            return w[:-3]
        elif word[-3:] in ["xo'"] and len(word) > 5:
            return w[:-3]
        elif word[-2:] in ["xo"] and len(word) > 5:
            return w[:-2]
        elif word[-2:] in ["en"] and len(word) > 5:
            return w[:-2]
        # nouns
        elif word[-2:] == 'in' and len(word) >= 5:
            return w[:-2]
        elif word[-2:] in ['iw', 'aw'] and len(word) >= 5:
            return w[:-2]
        else:
            return w

    def get_score(self, distance, w_len):
        if distance >= 5.0:
            return 0.0
        else:
            result = 1.0 - (distance/w_len * 1.5)
            if result < 0.0:
                return 0.0
            else:
                return result

    def get_levenshtein(self, w):
        # w is word as series
        logging.debug('w series:')
        logging.debug(w)
        current = self.df[self.df['series'].astype(str).str[0] == w[0]]
        current['ls_scores'] = current['series'].apply(levenshtein.levenshtein, 
                                                           args=(w,))
        logging.debug('FOUND!!!!')
        logging.debug(current['ls_scores'])
        try:
            found = current.nsmallest(1, 'ls_scores').iloc[0, :] # use keep='all' when I'm ready to support ties
        except TypeError: # if a vowel somehow ends up as initial
            w = ["'"] + w
            current = self.df[self.df['series'].astype(str).str[0] == w[0]]
            current['ls_scores'] = current['series'].apply(levenshtein.levenshtein, 
                                                               args=(w,))
            found = current.nsmallest(1, 'ls_scores').iloc[0, :] 
        logging.debug(current.nsmallest(5, 'ls_scores'))
        return found

    def match_word(self, word):
#        word = self.quick_stem(word)
        if '_ws' not in dir(self):
            self._ws = WordSeries.WordSeries()
        w = self._ws.get_series(word.lower())
        logging.debug('word series: ' + ''.join(w))

        finds = self.df[self.df['series'] == ''.join(w)]

        if len(finds) == 0:
            # this approach doesn't yet handle t vs tr confusion
            # this approach biases toward verbal nouns (xat) rather than verbs (xata) if conjugated (xathin)
            #    could solve this by recognizing POS
            # 'am and 'om represent unique problems
            # also k`itr`aw
            # examples like tr`i should bias in favor of y or ' finals
            #    could be a matter of tie-breaking once implemented
            # this fails completely on tahan for obvious reasons
            # also fails on wiya'an transcription variants
            # what is noc'i'?
            # also failed on wō'ihun (wo:'uyhun)
            found = self.get_levenshtein(w)
            if self.get_score(found['ls_scores'], len(found['series'])) <= 0.7:
                found_compare = self.get_levenshtein(self.quick_stem_series(w))
                if found_compare['ls_scores'] < found['ls_scores']:
                    found = found_compare
            result_word = found['word']
            meaning = found['meaning']
            score = self.get_score(found['ls_scores'], len(found['series']))
        else:
            found = finds.iloc[0, :]
            result_word = found['word']
            meaning = found['meaning']
            score = 1.0

        logging.debug('word matched string: ' + found['word'])

        return result_word + '\t' + meaning + '\t' + '{:.1f}%'.format(score * 100)

    def process_file_data(self, data, filename):
        results = []
        for word in data:
            if word in string.punctuation:
                results.append(word + '\t[punc]\t100.0%')
            elif word[0] in string.digits:
                results.append(word + '\t[digits]\t100.0%')
            elif word[0] in 'aeiouAEIOU' or 'v' in word or 'V' in word or 'f' in word or 'F' in word or 'Chi' in word or 'z' in word or 'Z' in word:
                results.append(word + '\t[foreign]\t100.0%')
            else:
                results.append(self.match_word(word))
        product = zip(data, results)
        f = open('../processed_data/' + filename, 'w')
        for line in product:
            f.write('\t'.join(line) + '\n')
        f.close()

if __name__ == '__main__':
    m = Matcher()
    if sys.argv[1] == '-w':
        print(m.match_word(sys.argv[2]))
    if sys.argv[1] == '-f':
        try:
            content = m.file_prep(sys.argv[2])
            logging.debug(content[-3:])
            m.process_file_data(content, sys.argv[2])
        except:
            raise 

