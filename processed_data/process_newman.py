
import pandas as pd

def find_non_matches(filename):
    df = pd.read_csv(filename, sep='\t', header=None)
    df.columns = ['original', 'matched', 'gloss', 'certainty']
    df['certainty'] = df['certainty'].apply(lambda x: float(x[:-1])/100)
    return df[df['certainty'] < 1.0]

if __name__ == '__main__':
    result = find_non_matches('Newman_3_preprocess.txt')
    result.to_csv('Newman_3_mismatches.txt', sep='\t', header=None)
    
