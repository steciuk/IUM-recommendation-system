import math
from sklearn.model_selection import train_test_split
import pandas as pd
from utils.readers.pandas_reader import read_users
from utils.readers.pandas_reader import read_sessions
from utils.readers.pandas_reader import read_products
from services.models.config import SEED
from services.models.config import MIN_INTERACTIONS
from services.models.config import TEST_SET_SIZE
from services.models.config import EVENT_TYPE_STRENGTH
from definitions import ROOT_DIR



def remove_rows_with_missing_values_of_attribute(dataset, attribute):
    return dataset[dataset[attribute].notna()]


def change_column_types(dataset, types):
    return dataset.astype(types)


def reconstruct_sessions_with_missing_user_id(sessions):
    sessions_copy = sessions.copy()
    missing = sessions[sessions['user_id'].isna()]
    for i, session in missing.iterrows():
        sessions_with_same_id = sessions[sessions['session_id'] == session['session_id']]
        for j, session_with_same_id in sessions_with_same_id.iterrows():
            if pd.notna(session_with_same_id['user_id']):
                sessions_copy.at[i, 'user_id'] = session_with_same_id['user_id']
                break

    return sessions_copy


def construct_0_1_data_matrix(users, products, sessions):
    data_matrix = pd.DataFrame(index=users['user_id'], columns=products['product_id'])
    for index, session in sessions.iterrows():
        if session['user_id'] in data_matrix.index and session['product_id'] in data_matrix.columns:
            data_matrix.at[session['user_id'], session['product_id']] = 1

    data_matrix = data_matrix.fillna(0)
    return data_matrix


def smooth_user_preference(x):
    return math.log(1 + x, 2)


def prepare_datasets():
    products = read_products()
    sessions = read_sessions()
    users = read_users()

    # products = products.drop(columns=['product_name', 'price'])
    sessions = sessions.drop(columns=['offered_discount', 'purchase_id', 'timestamp'])
    users = users.drop(columns=['name', 'city', 'street'])
    sessions = remove_rows_with_missing_values_of_attribute(sessions, 'product_id')
    sessions = reconstruct_sessions_with_missing_user_id(sessions)
    sessions = remove_rows_with_missing_values_of_attribute(sessions, 'user_id')
    sessions = change_column_types(sessions, {'user_id': int, 'product_id': int})

    return products, sessions, users


class DataHandler:
    def __init__(self):
        self.products, sessions, self.users = prepare_datasets()

        # TEMP1:
        # sessions.to_csv('temp_sessions.csv', index=False)
        # self.products.to_csv('temp_products.csv', index=False)
        # self.users.to_csv('temp_users.csv', index=False)

        # #TEMP2:
        # self.products = pd.read_csv(f'{ROOT_DIR}/temp_products.csv')
        # self.users = pd.read_csv(f'{ROOT_DIR}/temp_users.csv')
        # sessions = pd.read_csv(f'{ROOT_DIR}/temp_sessions.csv')

        sessions['event_strength'] = sessions['event_type'].apply(lambda x: EVENT_TYPE_STRENGTH[x])
        sessions = sessions.drop(columns='event_type')

        users_interactions_count = sessions.groupby(['user_id', 'product_id']).size().groupby('user_id').size()
        users_with_enough_interactions = \
            users_interactions_count[users_interactions_count >= MIN_INTERACTIONS].reset_index()[['user_id']]
        interactions = sessions.merge(users_with_enough_interactions, how='right', left_on='user_id',
                                      right_on='user_id')

        self.interactions = interactions.groupby(['user_id', 'product_id'])['event_strength'].sum().apply(
            smooth_user_preference).reset_index()

        interactions_train, interactions_test = train_test_split(interactions, stratify=interactions['user_id'],
                                                                 test_size=TEST_SET_SIZE, random_state=SEED)

        # Indexing by user_id to speed up the searches during evaluation
        self.interactions_indexed = self.interactions.set_index('user_id')
        self.interactions_train_indexed = interactions_train.set_index('user_id')
        self.interactions_test_indexed = interactions_test.set_index('user_id')
        self.item_popularity = self.interactions.groupby('product_id')['event_strength'].sum().sort_values(ascending=False).reset_index()
        self.item_ids = self.products['product_id'].tolist()

    def get_items_interacted(self, user_id, dataset):
        interacted_items = dataset.loc[user_id]['product_id']
        return set(interacted_items if type(interacted_items) == pd.Series else [interacted_items])
