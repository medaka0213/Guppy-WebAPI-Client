import re
from bs4 import BeautifulSoup
import urllib.request as req


def string_between(target, a,b):
    return target.split(a)[-1].split(b)[0]

def dollar():
    url="https://info.finance.yahoo.co.jp/fx/detail/?code=USDJPY=FX"
    res = req.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser');
    values = soup.select_one("#USDJPY_detail_bid").findAll(text=True)
    rate = float(''.join(values))
    return rate

def extract_floats(string):
    string = string.replace(",", "").replace(" ", "")
    result = re.findall(r"[-+]?\d*\.\d+|\d+", string)
    return [float(i) for i in result]


# 接頭辞を除く
def remove_prefix(string, prefix):
    return string.split(prefix)[-1]