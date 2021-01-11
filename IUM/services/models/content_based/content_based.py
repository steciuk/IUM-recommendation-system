from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from services.models.content_based import profiler
from services.models.data_handler import DataHandler


class ContentBasedRecommender:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.vectorizer = TfidfVectorizer(analyzer='word',
                                          ngram_range=(1, 1),
                                          max_features=5000,
                                          tokenizer=lambda x: x.split(';'))

        self.tfidf_matrix = self.vectorizer.fit_transform(data_handler.products['category_path'])
        self.tfidf_feature_names = self.vectorizer.get_feature_names()

        self.train_set = self.data_handler.interactions_indexed

        self.user_profiles = profiler.build_users_profiles(self.tfidf_matrix, self.data_handler.item_ids,
                                                          self.train_set)



    def _get_similar_items_to_user_profile(self, person_id, topn=1000):
        # Computes the cosine similarity between the user profile and all item profiles
        cosine_similarities = cosine_similarity(self.user_profiles[person_id], self.tfidf_matrix)
        # Gets the top similar items
        similar_indices = cosine_similarities.argsort().flatten()[-topn:]
        # Sort the similar items by similarity
        similar_items = sorted([(self.data_handler.item_ids[i], cosine_similarities[0, i]) for i in similar_indices], key=lambda x: -x[1])
        return similar_items

    def recommend_items(self, user_id, n=None):
        similar_items = self._get_similar_items_to_user_profile(user_id)
        # Ignores items the user has already interacted
        # items_seen = self.data_handler.get_items_interacted(user_id, self.train_set)
        items_seen = {}
        similar_items_filtered = list(filter(lambda x: x[0] not in items_seen, similar_items))
        recommendations_df = pd.DataFrame(similar_items_filtered, columns=['product_id', 'rec_strength'])

        if n is None:
            return recommendations_df
        else:
            return list(recommendations_df['product_id'].head(n) if n < len(recommendations_df) else recommendations_df[
                'product_id'])

