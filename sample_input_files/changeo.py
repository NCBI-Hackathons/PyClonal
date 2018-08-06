import os

import pandas as pd

def combineDir(directory):
    files = []
    for fn in os.listdir(directory):
        if not fn.endswith(".changeo.tsv"):
            continue
        files.append(fn)
    return combineFiles(files)

def combineFiles(files):
    sequence_indices = {}
    samples = {}

    for fn in files:
        print "Loading", fn
        df = pd.read_table(fn)

        for row in df.itertuples():
            if row.SAMPLE not in samples:
                samples[row.SAMPLE] = {"Sample": row.SAMPLE}

            seq = row.CLONE_CDR3_AA

            if seq not in sequence_indices:
                sequence_indices[seq] = len(sequence_indices)

            seq_idx = sequence_indices[seq]

            sample = samples[row.SAMPLE]
            sample[seq_idx] = sample.get(seq_idx, 0) + row.DUPCOUNT

    samples_df = pd.DataFrame(samples.values())
    samples_df = samples_df.set_index("Sample").fillna(0)

    sequences_df = pd.DataFrame(
            sorted([(v, k) for (k, v) in sequence_indices.items()]),
            columns=["Index", "Sequence"])
    sequences_df = sequences_df.set_index("Index")

    return samples_df, sequences_df

if __name__ == "__main__":
    samples_df, sequences_df = combineDir('.')

    samples_df.to_csv("changeo_combined.samples.tsv", sep="\t")
    sequences_df.to_csv("changeo_combined.sequences.tsv", sep="\t")
