import json


def j_writer(f, silent=False):

    def wrapper(*args, **kwargs):

        res = f(*args)
        if not res: return
        _j, name = res

        j = json.dumps(_j, indent=4, sort_keys=True, ensure_ascii=False, *kwargs)
        if not name.endswith('.json'):
            name += '.json'
        with open(name, 'w') as obj:
            obj.write(j)
        return 'JSON writer: saved {} to file'.format(name)

    return wrapper
