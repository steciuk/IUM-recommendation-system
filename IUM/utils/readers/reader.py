import json
import os

ROOT_DIR = os.path.abspath(os.curdir)


def read_users():
    with open(f'{ROOT_DIR}/data/users.json', encoding='utf-8') as f:
        data = json.load(f)
    f.close()
    return data


def read_products():
    with open(f'{ROOT_DIR}/data/products.json', encoding='utf-8') as f:
        data = json.load(f)
    f.close()
    return data


def read_sessions():
    with open(f'{ROOT_DIR}/data/sessions.json', encoding='utf-8') as f:
        data = json.load(f)
    f.close()
    return data
