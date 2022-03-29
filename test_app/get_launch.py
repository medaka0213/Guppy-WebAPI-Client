import unittest
from vrw_web_client import *
import logging
from tabulate import tabulate

logging.basicConfig(level=logging.INFO)

class SampleTest(unittest.TestCase):
    def test(self):
        logging.info('test_get_rocket')
        
        res = api.get("launch")
        logging.info(res)
        data = res["Items"]

        print(tabulate(data, headers='keys'))
        self.assertEqual(1, 1)