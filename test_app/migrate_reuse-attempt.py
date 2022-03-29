import unittest
from vrw_web_client import *
import logging

logging.basicConfig(level=logging.INFO)

import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

OLD_TABLE = "JRtP-Reuse-Attemps"
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
    change_dict_key(data, "result_type", "result")
    change_dict_key(data, "landed_at", "pad")
    change_dict_key(data, "vehicleName", "reuse-vehicle")

    if "vehicleID" in data: del data["vehicleID"]

    data["launch"] = "a" + data["missionID"].split("_")[1]
    data["unique"] = "launch_" + data["launch"] + "_" + data["reuse-vehicle"]
    return data


def print_dict(data):
    for k, v in data.items():
        if isinstance(v, list):
            print(f"{k}")
            for item in v:
                print(item[:30])
        else:
            print(f"{k}: {str(v)[:30]}")

class SampleTest(unittest.TestCase):
    def test(self):
        items = get_all_items()
        items = items
        items = [serialize_data(item) for item in items]

        item = ReuseAttempt()
        res = item.batch_put(items)

        self.assertEqual(1, 1)
        