from definitions import ROOT_DIR
from services.models.data_handler import DataHandler
from services.models.content_based.content_based import ContentBasedRecommender
from services.models.content_based import profiler


dh = DataHandler()
content_model = ContentBasedRecommender(dh)
user_id = 101

print("Users profile:")
profiler.print_profile(content_model.tfidf_feature_names, content_model.user_profiles, user_id)

recomended = content_model.recommend_items(user_id)
print("Recomended items:")
print(recomended[['product_id', 'rec_strength']].head(30))
recomended.to_csv(f'{ROOT_DIR}/services/models/content_based/CB_recs.csv', index=False, encoding='utf-8')


