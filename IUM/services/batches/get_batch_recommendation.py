import json
from definitions import ROOT_DIR
from services.models.model_type import Model_type


def get_batch_recommendation(user_id, model):
    if user_id < 101 or user_id > 1101:
        return []

    if model == Model_type.POPULARITY:
        file_name = 'popularity_batch.json'
        return read_batch(file_name, user_id)

    if model == Model_type.CONTENT_BASE:
        file_name = 'content_base_batch.json'
        return read_batch(file_name, user_id)


def read_batch(file_name, user_id):
    with open(f'{ROOT_DIR}/services/batches/{file_name}', mode="r") as f:
        data = json.load(f)
        user_recommendation = data[str(user_id)]
    f.close()

    return user_recommendation
