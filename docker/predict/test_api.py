import requests as r
from pprint import pprint

import unittest


class TestAPI(unittest.TestCase):

    def setUp(self):
        # self.nlp_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/dev_dnn_nlp'

        self.nlp_api = 'http://localhost:7007'

    def test_valid(self):

        results = r.post(
            self.nlp_api,
            json={
                'url1':
                    'aliens man, lizard people and chemtrails pesticide cancer illuminati free your mind sheep',
                'url2':
                    '''science genetics biometrics review biology statistical confidence evolution dna research professor'''
            })
        self.assertTrue(results.ok)
        # Check for 17 labels in resulting scores
        self.assertEqual(len(results.json()[0]['score']), 17)


unittest.main()