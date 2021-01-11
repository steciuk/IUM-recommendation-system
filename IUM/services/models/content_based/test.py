from services.models.data_handler import DataHandler
from services.models.content_based.content_based import ContentBasedRecommender

dh = DataHandler()
content_model = ContentBasedRecommender(dh)

print(content_model.recommend_items(user_id=102, n=5))