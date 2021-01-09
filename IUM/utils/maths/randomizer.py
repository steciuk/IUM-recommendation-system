from random import randrange
import copy

def random_sessions(sessions):
    sessions_copy = copy.deepcopy(sessions)

    for session in sessions_copy:
        session['product_id'] = randrange(1000, 1300)
    return sessions_copy
