from services.models.config import SEED


class RandomRecommender:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.name = "Random"

    def recommend_items(self, user_id, n=None):
        recommendations_df = self.data_handler.products.sample(frac=1.0, random_state=SEED)

        if n is None:
            return recommendations_df
        else:
            return list(recommendations_df['product_id'].head(n) if n < len(recommendations_df) else recommendations_df[
                'product_id'])
