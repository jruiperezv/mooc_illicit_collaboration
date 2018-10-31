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
    pivot_index = "session_user_id"
    df.columns = quiz_submission_meta_colnames
    df["submission_time"] = df["submission_time"].astype(int)
    # keep only most recent submission for each user https://stackoverflow.com/questions/32459325/python-pandas-dataframe-select-row-by-max-value-in-group/32459442
    df = df.loc[df.groupby(pivot_index)["submission_time"].idxmax()]
    df = df.pivot(index=pivot_index, columns="item_id", values="submission_time").reset_index()
    # add prefix
    df.rename(columns={x:"item_id_"+x for x in df.columns if x != pivot_index}, inplace=True)
    return df


