from typing import List, Optional
from pydantic import BaseModel, Field

# データベースのモデル
class VRWBaseModel(BaseModel):
    pk: str = ""
    sk: str = ""
    unique: str = ""

    def __getitem__(self, item):
        return getattr(self, item)
    
    def get(self, key: str, default=None):
        return self.dict().get(key) or default
    
    def get_jp(self, key: str, default=None):
        data = self.dict()
        return data.get(key+"_JP") or data.get(key+"_jp") or data.get(key) or default


# データベースのモデル (時間あり)
class DatetimeBaseModel(VRWBaseModel):
    datetime: str = None
    datetime_format: str = ""
    datetime_format_JP: str = ""
    datetime_time_type: str = "CONFIRMED"
    datetime_date_type: str = "CONFIRMED"
    datetime_isNET: bool  = False


# その他イベント
class event(DatetimeBaseModel):
    NextSpaceFlight: str = ""
    name: str = ""
    name_JP: str = None
    
    site: str = ""
    site_JP: str = None

    overview: str = ""
    overview_JP: str = None

    calendar: str = ""
    calendar_JP: str = ""

    watch_URL: str = None
    watch_URL_liftoff_at: int = None
    watch_URL_short: str = None

    image_url: str = None
    image_credit: str = None

    result: str = "PLANNED"


# 打ち上げ
class launch(event):
    rocket: str = ""
    rocket_JP: str = None

    provider: str = ""
    provider_JP: str = None

#カウントダウン
class countdwon_item(BaseModel):
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0
    
    desc_jp: str = ""
    desc_en: str = ""


# カウントダウンのモデル
class countdwon(VRWBaseModel):
    launch: str = ""
    event: str = ""

    t_minus: List[countdwon_item] = []
    t_plus: List[countdwon_item] = []


# カウントダウンのモデル
class countdwon(VRWBaseModel):
    launch: str = ""
    event: str = ""

    t_minus: List[countdwon_item] = []
    t_plus: List[countdwon_item] = []

# 集会のモデル
class meetup(VRWBaseModel):
    launch: str = ""
    event: str = ""

    type: str = "live"
    user: str = ""
    missionID: str = ""
    
    name: str = ""
    name_JP: str = ""

    title: str = ""
    title_JP: str = ""

    image_url: str = ""
    image_credit: str = ""

    calendar: str = ""
    calendar_JP: str = ""

    tweet: str = ""
    tweet_JP: str = ""

    isThumbDone : bool = False
    isTweetDone : bool = False
    isPosterDone : bool = False
    isVRCEveDone : bool = False
    isSlideDone : bool = False
    isCountDownDone : bool = False


def get(key):
    import sys
    try:
        return getattr(sys.modules[__name__], key)
    except AttributeError:
        return dict

def parse(target:dict):
    key = target.get("sk").replace("_item", "")
    schema = get(key)
    return schema(**target)
