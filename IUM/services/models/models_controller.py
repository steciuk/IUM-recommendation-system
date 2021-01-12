from services.models.data_handler import DataHandler
from services.models.popularity.popularity import PopularityRecommender
from services.models.content_based.content_based import ContentBasedRecommender
from services.models.model_type import Model_type


def get_recommendations(user_id, model):
    dh = DataHandler()
    popularity_model = PopularityRecommender(dh)
    content_base_model = ContentBasedRecommender(dh)

    if model == Model_type.POPULARITY:
        return popularity_model.recommend_items(user_id, 10)

    if model == Model_type.CONTENT_BASE:
        return content_base_model.recommend_items(user_id, 10)

    return NameError();
