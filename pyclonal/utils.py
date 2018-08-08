from __future__ import print_function
import itertools
import pandas as pd
from scipy.spatial.distance import cosine, jaccard
import numpy as np

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

def shannon_entropy(x):
    if x == 0:
        pass
    else:
        return np.log2(x) * x

def calc_clonality(df):
    df['sum']=df.sum(axis=1)
    norm_df=df.iloc[:,:-1].div(df["sum"], axis=0).transpose()
    se=norm_df
    for name in norm_df.columns:
        se[name]=norm_df[name].apply(lambda x: shannon_entropy(x))
    entropy=pd.DataFrame(-se.sum())
    maxentropy=-np.log2(1/(pd.DataFrame((df > 0).sum(axis=1))))
    final=1-entropy/maxentropy
    final.columns=['Clonality']
    return final
