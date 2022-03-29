import vrw_web_client.api as api 

import urllib.parse as urlparse

class vrwObject:
    def __init__(self, type):
        self.type = type

    def describe(self):
        path = self.type + "/describe"
        return api.get(path).get("Item", {})

    def get_list(self):
        return api.get(self.type).get("Items", [])
        
    def get_by_id(self, id):
        path = self.type +"/i/"+ id
        return api.get(path).get("Item", {})
    
    def get_by_unique(self, value):
        path = self.type +"/search/unique/" +  value
        res = api.get(path).get("Items", [])
        if len(res):
            return res[0]
        else:
            return {} 

    def put(self, submission, **kwargs):
        res = api.post(self.type, {
            "submission": submission,
            **kwargs
        })
        if res.get("result"):
            return res.get("Item")
        else:
            return res

    def post(self, submission, **kwargs):
        res = api.post(self.type, {
            "submission": submission,
            **kwargs
        })
        if res.get("result"):
            return res.get("Item")
        else:
            return res

    def batch_post(self, submission):
        """
        submission: list
        """
        path = self.type + "/batch"
        print("POST:", path)
        return api.post(path, {
            "submission": submission
        })

    def batch_put(self, submission):
        """
        submission: list
        """
        path = self.type + "/batch"
        print("POST:", path)
        return api.put(path, {
            "submission": submission
        })
    
    def delete(self, id):
        path = self.type +"/i/"+ id
        return api.delete(path)

    # 関連アイテムを適用
    def get_rel_items(self, item):
        """
        target: dict or str
        対象のアイテムに関連しているアイテムを取得
        """
        if isinstance(item, dict):
            item = item["pk"]

        path = self.type +"/i/" + item +  "/rel"
        print("GET:", path)
        return api.get(path).get("Items", [])

    # 関連アイテムを適用
    def put_rel_item(self, target, item):
        """
        target: dict
        item: dict
        対象のアイテムにターゲットのアイテムを関連付ける
        """
        path = self.type +"/i/" + item["pk"] +  "/rel"
        print("PUT:", path)
        return api.post(path, {
            "submission": {
                "pk": target["pk"],
            }
        })
    
    # 関連アイテムを削除
    def delete_rel_item(self, target, item):
        """
        target: dict
        item: dict
        対象のアイテムからターゲットのアイテムの関連付けを削除
        """
        path = self.type +"/i/" + item["pk"] +  "/rel"
        print("PUT:", path)
        return api.delete(path, {
            "submission": {
                "pk": target["pk"],
            }
        })
    
    # 参照アイテムをGEI
    def get_ref_items(self, item):
        """
        item: dict or str
        対象のアイテムを参照しているアイテムを取得
        """
        if isinstance(item, dict):
            item = item["pk"]

        path = self.type +"/i/" + item +  "/ref"
        print("GET:", path)
        return api.get(path).get("Items", [])

    # 参照アイテムを適用
    def put_ref_item(self, target, item):
        """
        target: dict
        item: dict
        targetの関連アイテムにitemを追加
        """
        path = self.type +"/i/" + item["pk"] +  "/ref"
        print("PUT:", path)
        return api.post(path, {
            "submission": {
                "pk": target["pk"],
            }
        })
    
    # 参照アイテムを削除
    def delete_ref_item(self, target, item):
        """
        target: dict
        item: dict
        targetの関連アイテムからitemを削除
        """
        path = self.type +"/i/" + item["pk"] +  "/ref"
        print("PUT:", path)
        return api.delete(path, {
            "submission": {
                "pk": target["pk"],
            }
        })

class Launch(vrwObject):
    def __init__(self):
        super().__init__("launch")

class Rocket(vrwObject):
    def __init__(self):
        super().__init__("rocket")

class Image(vrwObject):
    def __init__(self):
        super().__init__("image")

class Meetup(vrwObject):
    def __init__(self):
        super().__init__("meetup")

class Slide(vrwObject):
    def __init__(self):
        super().__init__("slide")