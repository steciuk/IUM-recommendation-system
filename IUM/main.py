from services.models.data_handler import DataHandler
from services.models.First.popularity import PopularityRecommender

dh = DataHandler()
popularity_model = PopularityRecommender(dh)

recommendations = popularity_model.recommend_items(user_id=102, n=5)
print(recommendations)

