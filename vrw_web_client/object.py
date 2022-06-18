import vrw_web_client.api as api 

import urllib.parse as urlparse
import os

from .params import QueryType

class vrwObject(object):
    def __init__(self, type):
        self.type = type
        self.root_path = "/q/" + self.type
        self.filter_params = {}

    # 検索用のフィルター追加
    def filter(self, key, value, mode):
        """
        kwargs: dict
        検索条件を指定して検索
        """
        self.filter_params.update({
            key: {
                "value": value,
                "mode": mode
            }
        }) 
        return self

    def set_url(self, path=""):
        path = os.path.join(self.root_path, *path.split("/"))
        path = path.replace("\\", "/")
        return path

    def _get_item(self, path=""):
        path = self.set_url(path)
        print("path:", path)
        return api.get(path).get("Item", {})
    
    def _get_items_list(self, path=""):
        path = self.set_url(path)
        return api.get(path, self.filter_params).get("Items", [])
    
    def _post(self, path="", submission={}):
        path = self.set_url(path)
        return api.post(path, {
            "submission": submission
        })
    
    def _put(self, path="", submission={}, overwrite=False):
        path = self.set_url(path)
        return api.put(path, {
            "submission": submission
        }, params = {
            "overwrite": {
                "value": overwrite,
            }
        })
    
    def _delete(self, path=""):
        path = self.set_url(path)
        return api.delete(path)


    def describe(self):
        return self._get_item("describe")

    def get_list(self):
        return self._get_items_list()

    def get_by_id(self, id):
        return self._get_item("/i/"+ id)
    
    def get_by_unique(self, value):
        path = "/search/unique/" +  value
        res = self._get_items_list(path)
        if len(res):
            return res[0]
        else:
            return {} 

    def put(self, submission, overwrite=False):
        res = self._put(submission=submission, overwrite=overwrite)
        if res.get("result"):
            return res.get("Item")
        else:
            return res

    def post(self, submission):
        res = self._post(submission=submission)
        if res.get("result"):
            return res.get("Item")
        else:
            return res

    def batch_post(self, submission):
        """
        submission: list
        """
        res = self._post("batch", submission=submission)
        if res.get("result"):
            return res.get("Item")
        else:
            return res

    def batch_put(self, submission, overwrite=False):
        """
        submission: list
        """
        res = self._put("batch", submission=submission, overwrite=overwrite)
        if res.get("result"):
            return res.get("Item")
        else:
            return res
    
    def delete(self, id):
        path = "/i/"+ id
        return self._delete(path)

    # 関連アイテムを適用
    def get_rel_items(self, item, prefix=""):
        """
        target: dict or str
        対象のアイテムに関連しているアイテムを取得
        """
        if isinstance(item, dict):
            item = item["pk"]

        path = "/i/" + item +  "/rel/" + prefix
        return self._get_items_list(path)

    # 関連アイテムを適用
    def put_rel_item(self, target, item):
        """
        target: dict
        item: dict
        対象のアイテムにターゲットのアイテムを関連付ける
        """
        path = "/i/" + item["pk"] +  "/rel"
        submission = {
            "pk": target["pk"]
        }
        return self._put(path, submission=submission)
    
    # 関連アイテムを適用
    def post_rel_item(self, target, item):
        """
        target: dict
        item: dict
        対象のアイテムにターゲットのアイテムを関連付ける
        """
        path = "/i/" + item["pk"] +  "/rel"
        submission = {
            "pk": target["pk"]
        }
        return self._post(path, submission=submission)

    # 関連アイテムを削除
    def delete_rel_item(self, target, item):
        """
        target: dict
        item: dict
        対象のアイテムからターゲットのアイテムの関連付けを削除
        """
        path = "/i/" + item["pk"] +  "/rel"
        submission = {
            "pk": target["pk"]
        }
        return self._delete(path, submission=submission)
    
    # 参照アイテムをGEI
    def get_ref_items(self, item, prefix=""):
        """
        item: dict or str
        対象のアイテムを参照しているアイテムを取得
        """
        if isinstance(item, dict):
            item = item["pk"]

        path = "/i/" + item +  "/ref/" + prefix
        return self._get_items_list(path)

    # 参照アイテムを適用
    def post_ref_item(self, target, item):
        """
        target: dict
        item: dict
        targetの関連アイテムにitemを追加
        """
        path = "/i/" + item["pk"] +  "/ref"
        submission = {
            "pk": target["pk"]
        }
        return self._post(path, submission=submission)

    # 参照アイテムを適用
    def put_ref_item(self, target, item):
        """
        target: dict
        item: dict
        targetの関連アイテムにitemを追加
        """
        path = "/i/" + item["pk"] +  "/ref"
        submission = {
            "pk": target["pk"]
        }
        return self._put(path, submission=submission)
    
    # 参照アイテムを削除
    def delete_ref_item(self, target, item):
        """
        target: dict
        item: dict
        targetの関連アイテムからitemを削除
        """
        path = "/i/" + item["pk"] +  "/ref"
        submission = {
            "pk": target["pk"]
        }
        return self._delete(path, submission=submission)

