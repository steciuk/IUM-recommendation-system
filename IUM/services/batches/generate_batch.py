import json
from definitions import ROOT_DIR
from services.models.data_handler import DataHandler
from services.models.content_based.content_based import ContentBasedRecommender
from services.models.popularity.popularity import PopularityRecommender



def generate_batches():
    dh = DataHandler()
    print("Dh done")

    popularity_model = PopularityRecommender(dh)
    print("Popularity_model done")

    content_base_model = ContentBasedRecommender(dh)
    print("Content_base_model  done")

    popularity_file_name = 'popularity_batch.json'
    data = {user_id: popularity_model.recommend_items(user_id, 10) for user_id in range(101, 1102)}
    write_batch(data, popularity_file_name)
    print("popularity_model write to file done")

    content_base_file_name = 'content_base_batch.json'
    data = {user_id: content_base_model.recommend_items(user_id, 10) for user_id in range(101, 1102)}
    write_batch(data, content_base_file_name)
    print("Content_base_model write to file done")


def write_batch(data, file_name):
    with open(f'{ROOT_DIR}/services/batches/{file_name}', mode="w") as f:
        json.dump(data, f)
    f.close()


generate_batches()

