import unittest
from vrw_web_client import vrwObject
import logging

logging.basicConfig(level=logging.INFO)

class SampleTest(unittest.TestCase):
    def test(self):
        logging.info('test_get_rocket')
        
        res = vrwObject("launch").get_list()
        logging.info(res)
        self.assertEqual(1, 1)