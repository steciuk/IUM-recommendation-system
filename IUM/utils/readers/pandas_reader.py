import pandas as pd
from definitions import ROOT_DIR


def read_users():
    with open(f'{ROOT_DIR}/data/ver3/users.csv', encoding='utf-8') as f:
        data = pd.read_csv(f)
    f.close()
    return data


def read_products():
    with open(f'{ROOT_DIR}/data/ver3/products.csv', encoding='utf-8') as f:
        data = pd.read_csv(f)
    f.close()
    return data


def read_sessions():
    with open(f'{ROOT_DIR}/data/ver3/sessions.csv', encoding='utf-8') as f:
        data = pd.read_csv(f)
    f.close()
    return data
