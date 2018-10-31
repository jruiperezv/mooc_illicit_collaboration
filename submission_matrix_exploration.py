"""
Functions to perform exploratory analysis and visualization of submission matrices.
"""

import argparse
import pandas as pd
from sklearn.manifold import TSNE
from ggplot import *


def main(infile):
    df = pd.read_csv(infile).fillna(-10000000)
    uid_columns = ["session_user_id"]
    feat_cols = [x for x in df.columns if not x in uid_columns]
    # todo: tsne visualization
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=1000, learning_rate=500)
    tsne_results = tsne.fit_transform(df.loc[:,feat_cols].values)
    df_tsne = pd.DataFrame(tsne_results[:, 0:2])
    df_tsne.columns = ["x-tsne", "y-tsne"]
    chart = ggplot(df_tsne, aes(x='x-tsne', y='y-tsne')) \
            + geom_point(size=70, alpha=0.1) \
            + ggtitle("tSNE dimensions colored by digit")
    chart

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", required=True, help="path to a submission matrix csv file")
    args = parser.parse_args()
    main(args.infile)