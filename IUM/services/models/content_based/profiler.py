import scipy.sparse
import numpy as np
import sklearn
import pandas as pd


def get_item_profile(tfidf_matrix, item_ids, item_id):
    idx = item_ids.index(item_id)
    item_profile = tfidf_matrix[idx:idx + 1]
    return item_profile


def get_item_profiles(tfidf_matrix, item_ids, ids):
    item_profiles_list = [get_item_profile(tfidf_matrix, item_ids, x) for x in ids]
    item_profiles = scipy.sparse.vstack(item_profiles_list)
    return item_profiles


def build_users_profile(tfidf_matrix, item_ids, person_id, interactions_indexed_df):
    interactions_person_df = interactions_indexed_df.loc[person_id]
    user_item_profiles = get_item_profiles(tfidf_matrix, item_ids, interactions_person_df['product_id'])

    user_item_strengths = np.array(interactions_person_df['event_strength']).reshape(-1, 1)
    user_item_strengths_weighted_avg = np.sum(user_item_profiles.multiply(user_item_strengths), axis=0) / np.sum(
        user_item_strengths)
    user_profile_norm = sklearn.preprocessing.normalize(user_item_strengths_weighted_avg)
    return user_profile_norm


def build_users_profiles(tfidf_matrix, item_ids, interactions_indexed_df):
    user_profiles = {}
    for person_id in interactions_indexed_df.index.unique():
        user_profiles[person_id] = build_users_profile(tfidf_matrix, item_ids, person_id, interactions_indexed_df)
    return user_profiles


def print_profile(tfidf_feature_names, profiles, user_id):
    profile = profiles[user_id]
    print(profile.shape)
    out = pd.DataFrame(sorted(zip(tfidf_feature_names,
                            profiles[user_id].flatten().tolist()), key=lambda x: -x[1]),
                 columns=['token', 'relevance'])

    print(out)
