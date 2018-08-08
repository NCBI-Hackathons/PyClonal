import itertools
import pandas as pd
from scipy.spatial.distance import cosine, jaccard

def distance(data, metadata, field=None, value=None, method='cosine'):
    patient='D233'
    df = data.join(metadata)
    df = df[df[field]==value]
    df = df.iloc[:, :-len(metadata.columns)]
    res_df = {}
    if method == 'cosine':
        for l1, l2 in itertools.combinations(df.index, 2):
            res_df.setdefault(l2, {})[l1] = res_df.setdefault(l1, {})[l2] = 1 - cosine(
                list(df.loc[l1].values),
                list(df.loc[l2].values),
            )
        return pd.DataFrame(res_df).fillna(1)
    elif method == 'jaccard':
        for l1, l2 in itertools.combinations(df.index, 2):
            res_df.setdefault(l2, {})[l1] = res_df.setdefault(l1, {})[l2] = jaccard(
                list(df.loc[l1].values),
                list(df.loc[l2].values),
            )
        return pd.DataFrame(res_df).fillna(1)
