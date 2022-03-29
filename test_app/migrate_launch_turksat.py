from operator import imod
import unittest
from vrw_web_client import *
import logging
from tabulate import tabulate

logging.basicConfig(level=logging.INFO)


import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

OLD_TABLE = "vspLaunchEvents"
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

def get_all_launches():
    kwargs = {
        "KeyConditionExpression": Key("type").eq("launch"),
    }

    response = table.query(**kwargs)
    if len(response['Items']):
        res_data =  response['Items']
        while "LastEvaluatedKey" in response:
            response = table.query(**kwargs, ExclusiveStartKey=response['LastEvaluatedKey'])
            res_data += response['Items']
        return deserialize_item(res_data)
    else:
        return []



def get_old_data():
    logging.info('test_get_rocket')

def serialize_data(data):
    change_dict_key(data, "date_type", "datetime_date_type")
    change_dict_key(data, "time_type", "datetime_time_type")
    change_dict_key(data, "isNET", "datetime_isNET")
    change_dict_key(data, "date", "datetime_format")
    change_dict_key(data, "date_JP", "datetime_format_JP")
    
    change_dict_key(data, "eventID", "NextSpaceFlight")
    
    change_dict_key(data, "missionName", "name")
    change_dict_key(data, "missionName_JP", "name_JP")

    change_dict_key(data, "missionOverview", "name")
    change_dict_key(data, "missionOverview_JP", "name_JP")

    change_dict_key(data, "site", "pad")
    change_dict_key(data, "launchSite", "site")
    change_dict_key(data, "launchSite_JP", "site_JP")


    if "image_url" in data: del data["image_url"]
    if "image_credit" in data: del data["image_credit"]
    if "rocket_image_url" in data: del data["rocket_image_url"]
    
    del data["type"]

    return data

def extract_images(data):
    print("extract image: ", data["missionName"])
    print(data)
    import requests
    import traceback

    def detect_mime(path, default="image/jpeg"):
        import mimetypes
        path = path.split("?")[0]
        path = path.split("#")[0]
        path = path.split("/")[-1]
        return mimetypes.guess_type(path)[0] or default

    def binary_to_b64(s, isDataURL=True, mime="image/jpeg"):
        import base64
        body = base64.b64encode(s).decode().replace("'", "")

        if isDataURL:
            print(f"data:{mime};base64,")
            return f"data:{mime};base64,{body}"
        else:
            return body

    def download_image(url):
        res = requests.get(url)
        if res.status_code == 200:
            print("download image: success")
            mime = detect_mime(url)
            print("mime: ", mime)
            return binary_to_b64(res.content, mime = mime)
        else:
            raise Exception("download image: failed")


    image_data = {}
    if "rocket_image_url" in data:
        is_image_exists = True
        image_data["url"] = data["rocket_image_url"]
    elif "image_url" in data:
        is_image_exists = True
        image_data["url"] = data["image_url"]
        image_data["credit"] = data.get("image_credit", "")
    else:
        print("no image")
        is_image_exists = False
    
    if is_image_exists:
        print("image_data: ", image_data)
        try:
            dataUri = download_image(image_data["url"])
            image_data["dataUri"] = dataUri
            image_data["mime"] = dataUri.split(",")[0].split(":")[1].split(";")[0]
            del image_data["url"]
            return {
                "item":image_data
            }
        except Exception as e:
            return None
    else:
        return None

def post_launch(data):
    serialize_data(data)

    image_data = {}
    is_image_exists = False

    
    launch = Launch()
    res_data = launch.post(data)
    print(res_data)
    
    if is_image_exists:
        image = Image()
        image_data["name"] = res_data["pk"] + "_thumbnail"
        res_image = image.post(image_data)
        
        # 画像を登録
        Launch().put_rel_item(res_data, res_image)

def print_dict(data):
    for k, v in data.items():
        print(f"{k}: {v[:10]}")

class SampleTest(unittest.TestCase):
    def test(self):
        logging.info('test_get_rocket')
        items = get_all_launches()
        items = [serialize_data(item) for item in items]
        items = [i for i in items if i["NextSpaceFlight"] == "a104"]

        launch = Launch()
        res_launch = launch.batch_put(items)
        print(res_launch)
        self.assertEqual(1, 1)
        