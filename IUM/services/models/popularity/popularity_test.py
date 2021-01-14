from definitions import ROOT_DIR
from services.models.data_handler import DataHandler
from services.models.popularity.popularity import PopularityRecommender

dh = DataHandler()
popularity_model = PopularityRecommender(dh)

predictions = popularity_model.recommend_items(user_id=102)
print(predictions)

