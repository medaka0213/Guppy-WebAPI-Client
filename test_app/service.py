import unittest
from vrw_web_client import *
import vrw_web_client.schema as schema
import logging

logging.basicConfig(level=logging.INFO)

class SampleTest(unittest.TestCase):
    def test(self):
        launch: schema.launch = VRWClient("launch").get_by_id("launch_0717dcfe-2991-411b-b07b-f58c94aec806")
        print(launch.dict())
        self.assertEqual(1, 1)