from IUM.services.reader import read_users
from IUM.services.reader import read_products
from IUM.services.reader import read_sessions


def get_user_ids(_users):
    _user_ids = []
    for user in _users:
        _user_ids.append(user["user_id"])
    return _user_ids


def get_product_ids(_products):
    _product_ids = []
    for product in _products:
        _product_ids.append(product["product_id"])
    return _product_ids


users = read_users()
sessions = read_sessions()
products = read_products()

user_ids = get_user_ids(users)
product_ids = get_product_ids(products)

matrix = [[0] * len(products)] * len(users)

ses = 0
for session in sessions:
    if session["user_id"] is None or session["product_id"] is None:
        continue
    if session["user_id"] not in user_ids or session["product_id"] not in product_ids:
        "No such user or product!"
        continue
    matrix[user_ids.index(session["user_id"])][product_ids.index(session["product_id"])] = 1
    ses += 1

ones = 0
for user in matrix:
    for product in user:
        if product == 1:
            ones += 1

print(ones / (len(user_ids) * len(product_ids)))
