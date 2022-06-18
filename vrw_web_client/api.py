import os
import json

import requests
from urllib.parse import urlencode

from .params import generate_query_value

API_URL_PROD = "https://api.virtualrocketwatching.net/v0"
API_URL_DEV = "http://localhost:8000"

API_URL = os.environ.get("VRW_WEB_API_URL", API_URL_PROD)
API_KEY = os.environ.get("VRW_WEB_API_KEY", "")

def _set_url(path):
    url = os.path.join(API_URL, *path.split("/"))
    url = url.replace("\\", "/")
    return url

def get(path, params={}):
    url = _set_url(path)
    print("GET:", url)

    print(params)
    params = {
        k: generate_query_value(**v) for k, v in params.items()
    }
    url = '{}?{}'.format(url, urlencode(params))
    print(url)

    res = requests.get(
        url,
        headers = {
            "x-api-key": API_KEY
        }
    )
    return res.json()

def post(path, body, params={}):
    url = _set_url(path)
    print("POST:", url)

    params = {
        k: generate_query_value(**v) for k, v in params.items()
    }

    res = requests.post(
        '{}?{}'.format(url, urlencode(params)),
        data = json.dumps(body),
        headers={
            'Content-Type': 'application/json',
            "x-api-key": API_KEY
        }
    )
    return res.json()

def put(path, body, params={}):
    url = _set_url(path)
    print("PUT:", url)

    print(params)

    params = {
        k: generate_query_value(**v) for k, v in params.items()
    }
    res = requests.put(
        '{}?{}'.format(url, urlencode(params)),
        data = json.dumps(body),
        headers={
            'Content-Type': 'application/json',
            "x-api-key": API_KEY
        }
    )
    return res.json()


def delete(path, params={}):
    url = _set_url(path)
    print("DELETE:", url)

    params = {
        k: generate_query_value(**v) for k, v in params.items()
    }
    res = requests.delete(
        '{}?{}'.format(url, urlencode(params)),
        headers={
            'Content-Type': 'application/json',
            "x-api-key": API_KEY
        }
    )
    return res.json()
