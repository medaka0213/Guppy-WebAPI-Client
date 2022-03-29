from vrw_web_client import *

items = Spacecraft().get_list()
for item in items:
    print(item)
    Spacecraft().delete(item["pk"])