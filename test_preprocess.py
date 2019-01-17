import unittest 
import preprocess as p 

class TestPreprocess(unittest.TestCase):
    def setUp(self):
        pass 

    def test_parse_csv(self):
        csv_contents = "1, -1\n,this is a lot of text, 1\netc. -1\n"
        csv_correct = [
            ['1', '-1'],
            ['this is a lot of text', '1'],
            ['etc.', '-1']
        ]
        results = p.parse_csv(csv_contents)
        self.assertListEqual(csv_correct, results)
