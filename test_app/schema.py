import unittest
from vrw_web_client import *
import vrw_web_client.schema as schema
import logging

logging.basicConfig(level=logging.INFO)

class SampleTest(unittest.TestCase):
    def test(self):
        cls = schema.get("VRWBaseModel")
        print(cls)
        
        item: schema.VRWBaseModel = cls(pk = "aaa", sk="bbb", unique="ccc")
        print(item)
        print(item["pk"])
        print(item.get("aaaa"))
        print(item.get_jp("aaaa"))

        self.assertEqual(1, 1)