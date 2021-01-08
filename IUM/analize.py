import statistics

from services.reader import read_users
from services.reader import read_products
from services.reader import read_sessions
from collections import defaultdict

users = read_users()
sessions = read_sessions()
products = read_products()


def get_user_ids(users):
    user_ids = []
    for user in users:
        user_ids.append(user["user_id"])
    return user_ids


def get_product_ids(products):
    product_ids = []
    for product in products:
        product_ids.append(product["product_id"])
    return product_ids


def analyze():
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


def find_sessions(session_id):
    out = []
    for session in sessions:
        if session["session_id"] == session_id:
            out.append(session)
    return out


def analyze2():
    num = 0
    for session in sessions:
        if session["user_id"] is None:
            reconst = False
            sessions_with_same_id = find_sessions(session["session_id"])
            for ses in sessions_with_same_id:
                if ses["user_id"] is not None:
                    reconst = True

            if reconst:
                num += 1

    print(num)


def analyze3():
    num = 0
    for session in sessions:
        if session["user_id"] is None or session["product_id"] is None:
            num += 1

    print(num)


def get_dates():
    dates = []
    for session in sessions:
        dates.append(session["timestamp"].split("T", 1)[0])

    return dates


def analyze4():
    dates_num = defaultdict(int)
    for date in get_dates():
        dates_num[date] += 1

    nums = list(dates_num.values())
    print(statistics.mean(nums))

analyze4()
