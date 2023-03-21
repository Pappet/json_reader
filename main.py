import json


def read_json(file_path):
    # JSON von einer Datei laden
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def find_depth(obj, current_depth=1):
    if isinstance(obj, dict):
        max_depth = current_depth
        for key in obj:
            depth = find_depth(obj[key], current_depth + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    elif isinstance(obj, list):
        max_depth = current_depth
        for item in obj:
            depth = find_depth(item, current_depth + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    else:
        return current_depth


def extract_keys(obj, keys=None):
    if keys is None:
        keys = set()

    if isinstance(obj, dict):
        for key, value in obj.items():
            keys.add(key)
            extract_keys(value, keys)
    elif isinstance(obj, list):
        for item in obj:
            extract_keys(item, keys)

    return keys


def extract_values(obj, values=None):
    if values is None:
        values = []

    if isinstance(obj, dict):
        for value in obj.values():
            extract_values(value, values)
    elif isinstance(obj, list):
        for item in obj:
            extract_values(item, values)
    else:
        values.append(obj)

    return values


def extract_key_paths(obj, current_path=None, paths=None):
    if current_path is None:
        current_path = []
    if paths is None:
        paths = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = current_path + [key]
            paths.append(new_path)
            extract_key_paths(value, new_path, paths)
    elif isinstance(obj, list):
        for item in obj:
            extract_key_paths(item, current_path, paths)

    return paths


if __name__ == '__main__':
    path = "test.json"

    loaded_json = read_json(path)
    print(find_depth(loaded_json))
    print()
    keys = extract_keys(loaded_json)
    print(keys)
    print()
    key_paths = extract_key_paths(loaded_json)
    formatted_key_paths = ['.'.join(path) for path in key_paths]
    unique_key_paths = list(set(formatted_key_paths))
    print(unique_key_paths)
    print()
    values = extract_values(loaded_json)
    print(values)


