import os
import json

import urllib.request
import urllib.parse as urlparse


API_URL = os.environ.get("VRW_WEB_API_URL", "http://localhost:8000")
API_KEY = os.environ.get("VRW_WEB_API_KEY", "")

def get(path, params={}):
    url = urlparse.urljoin(API_URL, path)
    print("GET:", url)
    req = urllib.request.Request(
        '{}?{}'.format(url, urllib.parse.urlencode(params)),
        headers = {
            "x-api-key": API_KEY
        }
    )
    with urllib.request.urlopen(req) as res:
        body = json.load(res)
        return body

def post(path, body, params={}):
    url = urlparse.urljoin(API_URL, path)
    print("POST:", url)
    req = urllib.request.Request(
        '{}?{}'.format(url, urllib.parse.urlencode(params)),
        json.dumps(body).encode(),
        method='POST',
        headers={
            'Content-Type': 'application/json',
            "x-api-key": API_KEY
        }
    )

    with urllib.request.urlopen(req) as res:
        body = json.load(res)
        return body

def put(path, body, params={}):
    url = urlparse.urljoin(API_URL, path)
    print("PUT:", url)
    req = urllib.request.Request(
        '{}?{}'.format(url, urllib.parse.urlencode(params)),
        json.dumps(body).encode(),
        method='PUT',
        headers={
            'Content-Type': 'application/json',
            "x-api-key": API_KEY
        }
    )

    with urllib.request.urlopen(req) as res:
        body = json.load(res)
        return body


def delete(path, params={}):
    url = urlparse.urljoin(API_URL, path)
    print("DELETE:", url)
    req = urllib.request.Request(
        '{}?{}'.format(url, urllib.parse.urlencode(params)),
        method='DELETE',
        headers={
            "x-api-key": API_KEY
        }
    )
    with urllib.request.urlopen(req) as res:
        body = json.load(res)
        return body
