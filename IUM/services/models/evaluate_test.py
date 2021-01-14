from services.models.data_handler import DataHandler
from services.models.content_based.content_based import ContentBasedRecommender
from services.models.model_evaluator import ModelEvaluator
from services.models.popularity.popularity import PopularityRecommender
from services.models.random.random import RandomRecommender
from services.models.content_based.profiler import print_profile

dh = DataHandler()
content_model = ContentBasedRecommender(dh)
popularity_model = PopularityRecommender(dh)
random_model = RandomRecommender(dh)
me = ModelEvaluator(dh)

print(me.evaluate_model(popularity_model))
print()
print(me.evaluate_model(content_model))
print()
print(me.evaluate_model(random_model))

#print(me.evaluate_model_for_user(content_model, 101))

# print(content_model.recommend_items(user_id=101))
# print(popularity_model.recommend_items(user_id=102))