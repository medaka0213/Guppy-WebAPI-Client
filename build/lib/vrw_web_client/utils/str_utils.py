import re
import urllib.request as req


def string_between(target, a,b):
    return target.split(a)[-1].split(b)[0]

def extract_floats(string):
    string = string.replace(",", "").replace(" ", "")
    result = re.findall(r"[-+]?\d*\.\d+|\d+", string)
    return [float(i) for i in result]


# 接頭辞を除く
def remove_prefix(string, prefix):
    return string.split(prefix)[-1]