import unittest
from vrw_web_client import *
import logging

logging.basicConfig(level=logging.INFO)

import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

OLD_TABLE = "JRtP-MeetUps"
ITEM_CLASS = Meetup
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
    change_dict_key(data, "host", "user")
    change_dict_key(data, "calendar_jp", "calendar")
    change_dict_key(data, "created_at", "created-at")
    change_dict_key(data, "updated_at", "updated-at")

    data["unique"] = data["missionID"] + "_" + data["type"]
    
    if "title" in data: del data["title"]
    if "title_JP" in data: del data["title_JP"]
    
    change_dict_key(data, "tweetEN", "tweet")
    change_dict_key(data, "tweetJP", "tweet_JP")
    
    if "image_url" in data: del data["image_url"]
    if "image_url" in data: del data["image_url"]

    if "missionStartsAt" in data: del data["missionStartsAt"]

    return data

def extract_images(data):
    print("extract image: ", data.get("title", data.get("missionID")))
    print(data)
    import requests

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
    is_image_exists = False
    if "image_url" in data:
        is_image_exists = True
        image_data["url"] = data["image_url"]
        image_data["credit"] = data["image_credit"]

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

def print_dict(data):
    print("{")
    for k, v in data.items():
        print(f"  {k}: {v[:10]}")
    print("}")

class SampleTest(unittest.TestCase):
    def test(self):
        items = get_all_items()
        
        images = [extract_images(item) for item in items] 
        items = [serialize_data(item) for item in items]

        item = ITEM_CLASS()
        res_launch = item.batch_post(items)
        print(res_launch)

        for i, target in enumerate(res_launch["results"]):
            if images[i] is not None:
                image_data = images[i]["item"]
                image_data["name"] = target["Item"]["pk"] + "_thumbnail"

                print("item:", str(target["Item"]))
                print("image:")
                print_dict(image_data)

                # 画像を保存
                image = Image()
                res_image = image.post(image_data)
                print("res_image:", str(res_image))
                res_image_rel = item.put_rel_item(target["Item"], res_image)
                print("res_image_rel:", str(res_image_rel))

        self.assertEqual(1, 1)