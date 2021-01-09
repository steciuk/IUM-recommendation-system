import pandas as pd
from utils.readers.pandas_reader import read_users
from utils.readers.pandas_reader import read_sessions
from utils.readers.pandas_reader import read_products


def remove_rows_with_missing_values_of_attribute(dataset, attribute):
    return dataset[dataset[attribute].notna()].reset_index()


def change_column_types(dataset, types):
    return dataset.astype(types)


def reconstruct_sessions_with_missing_user_id(sessions):
    sessions_copy = sessions.copy()
    missing = sessions[sessions["user_id"].isna()]
    for i, session in missing.iterrows():
        sessions_with_same_id = sessions[sessions["session_id"] == session["session_id"]]
        for j, session_with_same_id in sessions_with_same_id.iterrows():
            if pd.notna(session_with_same_id["user_id"]):
                sessions_copy.at[i, "user_id"] = session_with_same_id["user_id"]
                break

    return sessions_copy





    # num = 0
    # for session in sessions:
    #     if session["user_id"] is None:
    #         reconst = False
    #         sessions_with_same_id = find_sessions(session["session_id"])
    #         for ses in sessions_with_same_id:
    #             if ses["user_id"] is not None:
    #                 reconst = True
    #
    #         if reconst:
    #             num += 1


def model():
    products = read_products()
    sessions = read_sessions()
    users = read_users()

    #sessions = change_column_types(sessions, {"user_id": int, "product_id": int})

    sessions = remove_rows_with_missing_values_of_attribute(sessions, "product_id")

    #sessions = remove_sessions_with_missing_attribute(sessions, "user_id")
    #floaters = sessions[sessions["user_id"] != sessions["user_id"].astype(int)]
    #print(floaters["user_id"])

    print(len(sessions))
    sessions = reconstruct_sessions_with_missing_user_id(sessions)
    sessions = remove_rows_with_missing_values_of_attribute(sessions, "user_id")
    print(len(sessions))


model()