import pandas as pd


class PopularityRecommender:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.name = "Popularity"

    def recommend_items(self, user_id, n=None):
        if user_id not in set(self.data_handler.interactions_test_indexed.index.unique().values):
            return []

        # items_seen = self.data_handler.get_items_interacted(user_id, self.data_handler.interactions_train_indexed)
        recommendations_df = self.data_handler.item_popularity.sort_values('event_strength', ascending=False)
                                                            #  ^[~self.data_handler.item_popularity['product_id'].isin(items_seen)]
        # recommendations_df = pd.merge(recommendations_df, self.data_handler.products, how="left", on='product_id')

        if n is None:
            return recommendations_df
        else:
            return list(recommendations_df['product_id'].head(n) if n < len(recommendations_df) else recommendations_df[
                'product_id'])
