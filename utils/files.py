import json
from datetime import datetime


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


def to_json(obj):
    return json.dumps(obj, default=dumper, indent=4, ensure_ascii=False)


def to_map(json_):
    return json.loads(json_)


def get_short_time_str(datetime_=datetime.now()):
    return datetime_.strftime("%H:%M:%S")


def get_long_time_str(datetime_=datetime.now()):
    return datetime_.strftime("%d_%m_%Y__%H_%M_%S")


def get_time_name(name, is_start):
    if is_start:
        time_name = "start_"
    else:
        time_name = "end_"
    return time_name + str(name)