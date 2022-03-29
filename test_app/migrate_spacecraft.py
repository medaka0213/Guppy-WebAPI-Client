import unittest
from vrw_web_client import *
import logging

logging.basicConfig(level=logging.INFO)

import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

OLD_TABLE = "JRtP-Spacecrafts"
ITEM_CLASS = Spacecraft
ddb = boto3.resource('dynamodb')
table = ddb.Table(OLD_TABLE)

def deserialize_item(data):
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            result[k] = deserialize_item(v)
    elif isinstance(data, list):
        result = [deserialize_item(v) for v in data ]
    elif isinstance(data, Decimal):
        result = float(data)
    else:
        result = data
    return result

def get_all_items():
    response = table.scan()
    if len(response['Items']):
        res_data =  response['Items']
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            res_data += response['Items']
        return deserialize_item(res_data)
    else:
        return []


def serialize_data(data):
    change_dict_key(data, "total_mass", "mass")
    
    missionID = data["missionID"]
    del data["missionID"]

    data["launch"] = "a" + missionID.split("_")[1]
    data["unique"] = "launch_" + data["launch"] + "_" + data["name"]
    
    if "count" in data:
        data["count"] = int(data["count"])

    return data

def print_dict(data):
    print("{")
    for k, v in data.items():
        print(f"  {k}: {v[:10]}")
    print("}")

class SampleTest(unittest.TestCase):
    def test(self):
        items = get_all_items()
        items = items[9:]
        
        items = [serialize_data(item) for item in items]

        item = ITEM_CLASS()
        for i in items:
            res = item.put(i)
            print(res)

        self.assertEqual(1, 1)