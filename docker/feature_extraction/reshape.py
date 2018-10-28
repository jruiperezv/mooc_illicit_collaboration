import pandas as pd
import os


def create_submission_matrix_from_query_result(fp):
    """

    :param fp:
    :return:
    """
    df = pd.read_csv(fp, dtype=object)
    quiz_submission_meta_colnames = ["id", "item_id", "session_user_id", "submission_time", "submission_number",
                                     "raw_score", "grading_error", "authenticated_submission_id"]
    pivot_index_colnames=["session_user_id", "id"]
    df.columns = quiz_submission_meta_colnames
    df["submission_time"] = df["submission_time"].astype(int)
    df = df.pivot_table(index=pivot_index_colnames, columns="item_id", values="submission_time").reset_index()
    # add prefix
    df.rename(columns={x:"quiz_"+x for x in df.columns if x not in pivot_index_colnames}, inplace=True)
    return df


