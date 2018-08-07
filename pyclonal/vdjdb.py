import os
import sys

import pandas as pd

"""
To download a new VDJdb database:
Go to https://vdjdb.cdr3.net/search and select "Export as:" -> TSV
And place the downloaded file at data/VDJdb.tsv
"""

def findEpitopes(sequences):
    """
    sequences: a pandas dataframe containing columns "Index" and "Sequence"
    """

    vdj_data = pd.read_table(os.path.join(os.path.dirname(__file__), "../data/VDJdb.tsv"))

    epitopes = {}
    for row in vdj_data.itertuples():
        epitopes[row.CDR3] = row.Epitope

    # print epitopes
    # print vdj_data.loc[vdj_data.index.intersection(["CASSYSRTGSYEQYF", "CASSLGGRGRGTEAF"])]["Epitope"]

    found_epitopes = []
    for row in sequences.itertuples():
        found_epitopes.append(epitopes.get(row.Sequence, ""))

    print filter(bool, found_epitopes)

    return found_epitopes

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python %s FILES" % sys.argv[0])
        sys.exit(1)

    sequences = pd.read_table(sys.argv[1])
    found_epitopes = findEpitopes(sequences)
    sequences['Epitope'] = pd.Series(found_epitopes, sequences.index)

    sequences.to_csv("sequences_with_epitopes.tsv", sep="\t", index=False)
