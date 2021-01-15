from services.models.model_type import Model_type

DIVIDER = 550


def get_user_model(user_id):
    if user_id > DIVIDER:
        return Model_type.CONTENT_BASE

    return Model_type.POPULARITY
