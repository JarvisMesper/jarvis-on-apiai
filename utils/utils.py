import json
import os


def save_json_file(path, filename, content):
    filename = path + filename
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(content, f, indent=4, sort_keys=True)


def open_json_file(path, filename):
    if not os.path.exists(path + filename):
        save_json_file(path, filename, {})

    with open(path + filename, encoding="utf-8") as f:
        data = json.load(f)
    return data
