import unittest

import WordSeries
import levenshtein

class TestLevenshtein(unittest.TestCase):
    def setUp(self):
        self.ws = WordSeries.WordSeries()

    def test_levenshtein(self):
        examples = [('hiyuk', 'hiyuk', 0),
                 ('hoho', 'hǫ:hǫ', 0),
                 ('waki', 'wakkiy', 2),
                 ('pokhin', "bok'o", 2),
                 ('pānahin', 'pana:', 3)]
        for item in examples:
            a = self.ws.get_series(item[0])
            b = self.ws.get_series(item[1])
            calc_dist = levenshtein.levenshtein(a, b)
            self.assertEqual(calc_dist, item[2])

if __name__ == '__main__':
    unittest.main()
