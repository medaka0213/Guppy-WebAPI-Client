# 辞書のキーを変える
def change_dict_key(dict, old_key, new_key):
    if old_key in dict:
        dict[new_key] = dict[old_key]
        del dict[old_key]
    return dict

# 辞書を指定したキーのリストから抽出
def extract_keys_from_dict(dict, *keys):
    result = {}
    for key in keys:
        if key in dict:
            result[key] = dict[key]
    return result

# 辞書から指定したキーのリストを削除
def remove_keys_from_dict(dict, *keys):
    for key in keys:
        if key in dict:
            del dict[key]
    return dict

# 辞書の同じ接頭辞からなるキーを抽出
def extract_dict_by_prefix(dict, prefix, preserve_keys = False):
    result = {}
    for key in dict.keys():
        if key.startswith(prefix):
            if preserve_keys:
                # 接頭辞を残す
                result[key] = dict[key]
            else:
                # 接頭辞を削除
                result[key[len(prefix):]] = dict[key]
    return result

# 辞書の同じ接尾辞からなるキーを抽出
def extract_dict_by_suffix(dict, suffix, preserve_keys = False):
    result = {}
    for key in dict.keys():
        if key.endswith(suffix):
            if preserve_keys:
                # 接尾辞を残す
                result[key] = dict[key]
            else:
                # 接尾辞を削除
                result[key[:-len(suffix)]] = dict[key]
    return result

# 同じ値のJSONか調べる
def is_same_json(data_0, data_1):
    if type(data_0) == dict or type(data_1) == dict:
        keys = list(set( list(data_0.keys()) + list(data_1.keys() )))

        for k in keys:
            #値がなければアウト
            if (not k in data_1) or (not k in data_0):
                return False
            
            if not is_same_json(data_0.get(k), data_1.get(k)):

                return False

    elif type(data_0) == list and type(data_1) == list:
        if len(data_0) != len(data_1):
            return False
        else:
            for v_0, v_1 in zip(data_0, data_1):
                if not is_same_json(v_1, v_0):
                    return False
    else:
        return data_0 == data_1
    
    return True

# 同じユニークキーの辞書か調べる
def is_same_unique_keys_dict(dict_0, dict_1, unique_keys = ["pk", "sk"]):
    for key in unique_keys:
        if not is_same_json(dict_0.get(key), dict_1.get(key)):
            return False
    return True



# 配列の差分を抽出
def list_difference(old_list, new_list):
    print(old_list)
    print(new_list)
    result = {
        "added": [],
        "removed": [],
        "same": [],
        "all": union_from_lists(old_list, new_list)
    }

    common_items = union_from_lists(old_list, new_list)
    for item in common_items:
        if item in old_list and item in new_list:
            result["same"].append(item)
        elif item in old_list:
            result["removed"].append(item)
        elif item in new_list:
            result["added"].append(item)
    return result


# 辞書の差分を抽出
def dict_difference(old_item, new_item):
    _result = list_difference(list(old_item.keys()), list(new_item.keys()))
    
    # 追加、削除されたキーはそのまま返す
    result = {
        "same": [],
        "changed": [],
        **extract_dict_by_keys(_result, "added", "removed", "all")
    }

    # 共通のキーは、値が同じか調べる
    for key in _result["same"]:
        if not is_same_json(old_item.get(key), new_item.get(key)):
            result["changed"].append(key)
        else:
            result["same"].append(key)

    return result



# 辞書を含む配列の差分を抽出
def json_difference(old_list, new_list, unique_keys = ["pk", "sk"]):
    result = {
        "added": [],
        "removed": [],
        "changed": [],
        "same": [],
        "all": old_list
    }

    # 古い配列から、新しい配列に含まれるものを抽出
    for o in old_list:
        n = [n for n in new_list if is_same_unique_keys_dict(o, n, unique_keys)]
        if len(n) == 0:
            result["removed"].append(o)
        else:
            if is_same_json(n[0], o):
                result["same"].append(o)
            else:
                result["changed"].append(o)

    # 新しい配列から、古い配列に含まれないものを抽出
    for n in new_list:
        o = [o for o in old_list if is_same_unique_keys_dict(o, n, unique_keys)]
        if len(o) == 0:
            result["added"].append(n)
            result["all"].append(n)
    return result
    
# 配列の共通部分を抽出
def extract_common_items_from_lists(*lists):
    items = set(lists[0])
    for _list in lists:
        items = items & set(_list)
    return list(items)

# 配列の和集合を求める
def union_from_lists(*lists):
    items = set(lists[0])
    for _list in lists:
        items = items | set(_list)
    return list(items)

# 辞書の複数キーを抽出
def extract_dict_by_keys(dict, *keys):
    common_keys = extract_common_items_from_lists(dict.keys(), keys) 
    result = {}
    for key in common_keys:
        result[key] = dict[key]
    return result

# 配列を検索
def search_array_by_func(array, func):
    for i, v in enumerate(array):
        if func(v):
            return i
    return -1

def search_array_by_value(array, value):
    return search_array_by_func(array, lambda v: v == value)

def search_array_by_value_in_list(array, value_list):
    return search_array_by_func(array, lambda v: v in value_list)

def search_array_by_value_not_in_list(array, value_list):
    return search_array_by_func(array, lambda v: v not in value_list)

def search_array_by_key_and_value(array, key, value):
    return search_array_by_func(array, lambda v: v[key] == value)

