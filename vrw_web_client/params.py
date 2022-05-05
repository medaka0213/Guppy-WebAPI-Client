#クエリ設定のENUM
from enum import Enum
class QueryType(Enum):
    """
    Enum for query types
    """
    EQ = "EQUAL"
    N_EQ = "NOT_EQUAL"
    IN = "IN"
    BETWEEN = "BETWEEN"
    CONTAINS = "CONTAINS"
    GT = "GREATER_THAN"
    GT_E = "GREATER_THAN_OR_EQUAL"
    LT = "LESS_THAN"
    LT_E = "LESS_THAN_OR_EQUAL"
    BEGINS = "BEGINS_WITH"
    EX = "EXISTS"
    N_EX = "NOT_EXISTS"

def generate_query_value(value, mode):
    # データの処理
    if isinstance(value, str):
        value= "\"" + str(value) + "\""
    elif isinstance(value, list):
        value= ["\"" + str(v) + "\"" for v in value if isinstance(v, str)]
    
    if mode == QueryType.LT_E or mode == QueryType.LT_E.value:
        result = "..." + str(value)
    elif mode == QueryType.GT_E or mode == QueryType.GT_E.value:
        result = str(value) + "..."
    elif mode == QueryType.BETWEEN or mode == QueryType.BETWEEN.value:
        v0 = min(value[0], value[1])
        v1 = max(value[0], value[1])
        result = str(v0) + "..." + str(v1)
        
    elif mode == QueryType.LT or mode == QueryType.LT.value:
        result = ".." + str(value)
    elif mode == QueryType.GT or mode == QueryType.GT.value:
        result = str(value) + ".."
    
    elif mode == QueryType.EX or mode == QueryType.EX.value:
        result = "*"
    elif mode == QueryType.N_EX or mode == QueryType.N_EX.value:
        result = "--"
    elif mode == QueryType.N_EQ or mode == QueryType.N_EQ.value:
        result = "--" + str(value)
    
    elif mode == QueryType.BEGINS or mode == QueryType.BEGINS.value:
        result = str(value) + "*"
    elif mode == QueryType.CONTAINS or mode == QueryType.CONTAINS.value:
        result = "*" + str(value) + "*"
    else:
        result = str(value)
    return result
