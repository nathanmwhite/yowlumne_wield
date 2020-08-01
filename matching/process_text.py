import logging

import WordSeries

logging.basicConfig(level=logging.DEBUG)

def process_text(filename):
    ws = WordSeries.WordSeries() # it would be nice to keep this in state when using elsewhere; use generator
    processed_text = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            current_processed_line = []
            for word in line.strip(' .\n').split(' '):
                current_word = word.strip('/').strip(',').strip('.')
                if len(current_word) > 0:
                    current_processed_line.append(''.join(ws.get_series(current_word)))
            processed_text.append(current_processed_line)
    return processed_text

if __name__ == '__main__':
    print(process_text('sample.txt'))
