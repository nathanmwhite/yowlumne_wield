import re

import pandas as pd
import numpy as np

import WordSeries

def prepare_df(df):
    # this needs to be redone so that it works elementwise on df 
    ws = WordSeries.WordSeries()
    data = []
    for item in df['word']:
        #print(item)
        current_word = item.strip('/').strip(',').strip('.')
        to_filter = ['\+', '\(', '\)', '\-', '\?', '[^aeiouáąǫ]:']
        for symbol in to_filter:
            current_word = re.sub(symbol, '', current_word)
        #print(current_word)
        result = ws.get_series(current_word)
        data.append(''.join(result))
    df['series'] = pd.Series(data)
    return df

if __name__ == '__main__':
    df = pd.read_csv('../raw_data/word_lists_csv/vocab.csv', sep='\t', index_col=0, keep_default_na=False, na_values=['_'])
    df = prepare_df(df)    
    print(df.loc[:, ['word', 'series']])
