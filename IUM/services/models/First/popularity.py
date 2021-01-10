from services.models.data_handler import DataHandler


class PopularityRecommender:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def recommend_items(self, user_id, n=None):
        items_seen = self.data_handler.get_items_interacted(user_id, self.data_handler.interactions_train_indexed)
        recommendations_df = self.data_handler.item_popularity.sort_values('event_strength', ascending=False)
                                                            #  ^[~self.data_handler.item_popularity['product_id'].isin(items_seen)]
        if n is None:
            return recommendations_df
        else:
            return list(recommendations_df['product_id'].head(n) if n < len(recommendations_df) else recommendations_df[
                'product_id'])
