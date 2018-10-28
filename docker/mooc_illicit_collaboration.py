from feature_extraction.sql_utils import *
from feature_extraction.reshape import create_submission_matrix_from_query_result
import os
import pandas as pd
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="execute feature extraction, training, or testing.")
    parser.add_argument("-c", "--course", required=False,
                        help="an s3 pointer to a course; not used but will be provided as 'None' by MORF")
    parser.add_argument("-r", "--session", required=False,
                        help="3-digit course run number; not used but will be provided as 'None' by MORF")
    parser.add_argument("-m", "--mode", required=True, help="mode to run image in; {extract, train, test}")
    args = parser.parse_args()
    if args.mode == "extract":
        # this block expects individual session-level data mounted by extract_session() and outputs one CSV file per session in /output
        # generate forum post CSV files for each session and aggregate into single file
        raw_submission_matrix_filename = "submission_matrix_raw.csv"
        raw_submission_matrix_fp = os.path.join("input", args.course, args.session, raw_submission_matrix_filename)
        extract_coursera_sql_data(args.course, args.session, outfile=raw_submission_matrix_filename)
        # postprocess sql results to form submission matrix by pivoting columns of csv
        submission_matrix = create_submission_matrix_from_query_result(raw_submission_matrix_fp)
        submission_matrix.to_csv(os.path.join("output", "submission_matrix.csv"), index=False)
        os.remove(raw_submission_matrix_fp)
    else: # this script should not be called in any other mode
        raise NotImplementedError
