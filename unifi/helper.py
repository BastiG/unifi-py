from json import dumps as json_dumps


def find_by_attr(data, _as_list=False, _path='data', **attrs):
    if _path:
        for el in _path.split('.'):
            if el in data:
                data = data[el]
            else:
                return None

    results = list(filter(lambda x: all([key in x and x[key] in [value, str(value)] for key, value in attrs.items()]), data))
    if _as_list:
        return results
    return results[0] if results else None

def json_print(json, indent=2):
    print(json_dumps(json, indent=indent, sort_keys=True))

