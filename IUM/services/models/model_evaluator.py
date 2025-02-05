from services.models.config import SEED
import random
import pandas as pd
from services.models.config import EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS


class ModelEvaluator:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def get_not_interacted_items_sample(self, person_id, sample_size, seed=SEED):
        interacted_items = self.data_handler.get_items_interacted(person_id, self.data_handler.interactions_indexed)
        all_items = set(self.data_handler.products['product_id'])
        non_interacted_items = all_items - interacted_items

        random.seed(seed)
        non_interacted_items_sample = random.sample(non_interacted_items, sample_size)
        return set(non_interacted_items_sample)

    def _verify_hit_top_n(self, item_id, recommended_items, top_n):
        try:
            index = next(i for i, c in enumerate(recommended_items) if c == item_id)
        except:
            index = -1
        hit = int(index in range(0, top_n))
        return hit, index

    def evaluate_model_for_user(self, model, person_id):
        interacted_values_test = self.data_handler.interactions_test_indexed.loc[person_id]
        if type(interacted_values_test['product_id']) == pd.Series:
            person_interacted_items_test = set(interacted_values_test['product_id'])
        else:
            person_interacted_items_test = set([int(interacted_values_test['product_id'])])

        interacted_items_count_test = len(person_interacted_items_test)

        person_recs_df = model.recommend_items(person_id)

        hits_at_5_count = 0
        hits_at_10_count = 0

        for item_id in person_interacted_items_test:
            non_interacted_items_sample = self.get_not_interacted_items_sample(person_id,
                                                                               sample_size=EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS,
                                                                               seed=item_id % (2 ** 32))

            items_to_filter_recs = non_interacted_items_sample.union({item_id})
            valid_recs_df = person_recs_df[person_recs_df['product_id'].isin(items_to_filter_recs)]

            valid_recs = valid_recs_df['product_id'].values

            hit_at_5, index_at_5 = self._verify_hit_top_n(item_id, valid_recs, 5)
            hits_at_5_count += hit_at_5
            hit_at_10, index_at_10 = self._verify_hit_top_n(item_id, valid_recs, 10)
            hits_at_10_count += hit_at_10

        recall_at_5 = hits_at_5_count / float(interacted_items_count_test)
        recall_at_10 = hits_at_10_count / float(interacted_items_count_test)

        person_metrics = {'hits@5_count': hits_at_5_count,
                          'hits@10_count': hits_at_10_count,
                          'interacted_count': interacted_items_count_test,
                          'recall@5': recall_at_5,
                          'recall@10': recall_at_10}
        return person_metrics

    def evaluate_model(self, model):
        print("Evaluated model:", model.name)
        people_metrics = []
        for idx, person_id in enumerate(list(self.data_handler.interactions_test_indexed.index.unique().values)):
            person_metrics = self.evaluate_model_for_user(model, person_id)
            person_metrics['_person_id'] = person_id
            people_metrics.append(person_metrics)
        print('%d users processed' % idx)

        detailed_results_df = pd.DataFrame(people_metrics).sort_values('interacted_count', ascending=False)

        global_recall_at_5 = detailed_results_df['hits@5_count'].sum() / float(detailed_results_df['interacted_count'].sum())
        global_recall_at_10 = detailed_results_df['hits@10_count'].sum() / float(detailed_results_df['interacted_count'].sum())

        global_metrics = {'recall@5': global_recall_at_5,
                          'recall@10': global_recall_at_10}
        return global_metrics
