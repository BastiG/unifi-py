from unifi.objects.base import UnifiBaseObject

from json import dumps as json_dumps

def find_by_attr(data, _as_list=False, _path=None, **attrs):
    def __get_attr(data, name):
        if isinstance(data, UnifiBaseObject) and hasattr(data, name):
            return True, getattr(data, name)
        elif isinstance(data, dict) and name in data:
            return True, data[name]
        elif isinstance(data, list) and (isinstance(name, int) or (isinstance(name, str) and name.isnumeric())) and int(name) < len(data):
            return True, data[name]
        else:
            return False, None

    if _path is None:
        if isinstance(data, dict) and 'data' in data:
            data = data['data']
    else:
        if isinstance(_path, str):
            _path = _path.split('.')
        for el in _path:
            found, data = __get_attr(data, el)
            if not found:
                return None

    results = []
    for item in data:
        found = True
        for filter_name, filter_value in attrs.items():
            found, value = __get_attr(item, filter_name)
            if not found or value not in [filter_value, str(filter_value)]:
                found = False
                break
        if found:
            results.append(item)
    
    if _as_list:
        return results
    return results[0] if results else None

def json_print(json, indent=2):
    print(json_dumps(json, indent=indent, sort_keys=True))

