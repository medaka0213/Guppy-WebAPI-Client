import unittest
from vrw_web_client import *
import logging

logging.basicConfig(level=logging.INFO)

import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

OLD_TABLE = "JRtP-Slides"
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



def extract_images(old_data):
    DIGITS = 5
    image_paths = [f"{old_data['type']}/{old_data['id']}/{str(index).zfill(DIGITS)}.jpg" for index in range(int(old_data['data_length']))]

    def binary_to_b64(s, isDataURL=True, mime="image/jpeg"):
        import base64
        body = base64.b64encode(s).decode().replace("'", "")

        if isDataURL:
            print(f"data:{mime};base64,")
            return f"data:{mime};base64,{body}"
        else:
            return body

    def download_image(url):
        import requests
        print(f"download image: {url}")
        res = requests.get(url)
        if res.status_code == 200:
            print("download image: success")
            return binary_to_b64(res.content, mime = "image/jpeg")
        else:
            raise Exception("download image: failed")

    old_s3_url = "https://vspliveview.s3.ap-northeast-1.amazonaws.com/images/slides_v2"
    image_paths = [f"{old_s3_url}/{path}" for path in image_paths]
    return [download_image(url) for url in image_paths]

def serialize_data(data):
    data["images"] = extract_images(data)

    change_dict_key(data, "created_at", "created-at")
    change_dict_key(data, "updated_at", "updated-at")
    change_dict_key(data, "data_length", "data-length")
    change_dict_key(data, "userName", "user")
    change_dict_key(data, "title", "name")

    data["unique"] = data["type"] + "_" + data["id"]
    del data["type"]
    del data["id"]

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

        item = Slide()
        res = item.batch_put(items)

        for _item in res["results"]:
            item = _item["Item"]
            print_dict(item)
            if item["unique"].startswith("launch_"):
                print(f"Add reference: {item['unique']}")
                id = item["unique"].split("_")[1]
                launch = Launch().get_by_unique(id)
                print_dict(item)
                res_ref = Slide().put_ref_item(launch, item)
                print_dict(res_ref)
        self.assertEqual(1, 1)
        