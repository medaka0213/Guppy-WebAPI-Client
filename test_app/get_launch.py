import unittest
from vrw_web_client import *
import logging

logging.basicConfig(level=logging.INFO)

class SampleTest(unittest.TestCase):
    def test(self):
        logging.info('test_get_rocket')
        
        res = vrwObject("launch").filter(
            "datetime", "2024-01-01", "GREATER_THAN_OR_EQUAL"
        ).filter(
            "datetime_date_type", "CONFIRMED", "EQUAL"
        ).get_list()
        logging.info(res)
        self.assertEqual(1, 1)