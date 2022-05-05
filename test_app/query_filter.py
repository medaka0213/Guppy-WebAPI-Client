import unittest
from vrw_web_client import *

class SampleTest(unittest.TestCase):
    def test(self):
        logging.info('test_get_rocket')
        
        res = vrwObject("launch").filter(
            "datetime", "2024-01-01", QueryType.GT_E
        ).filter(
            "datetime_date_type", "CONFIRMED", QueryType.EQ
        ).get_list()
        logging.info(res)
        self.assertEqual(1, 1)