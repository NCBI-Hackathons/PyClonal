import pandas as pd
from .parser import BaseParser


def combineFiles(filenames, fmt=None, fmt_cols=None):
    """
    Given a list of filenames, read and parse all of them.

    Returns: two dataframes, a samples dataframe and a sequences dataframe.

    The samples dataframe has one row per sample, and one column per unique clone.
    The sequences dataframe has one row per clone, mapping clone index to clone sequence.
    """

    sequence_indices = {}
    samples = {}

    for filename in filenames:
        parseFile(filename, sequence_indices, samples, fmt, fmt_cols)

    samples = sorted(samples.items())
    samples_df = pd.DataFrame([p[1] for p in samples])
    samples_df = samples_df.set_index("Sample").fillna(0)

    sequences_df = pd.DataFrame(
            sorted([(v, k) for (k, v) in sequence_indices.items()]),
            columns=["Index", "Sequence"])
    sequences_df = sequences_df.set_index("Index")

    return samples_df, sequences_df


def parseFile(filename, sequence_indices=None, samples=None, fmt=None,
        fmt_cols=None):
    """
    Parses a file, returning a sequence_id => count mapping.

    Accumulates the results in `sequence_indices` and `samples` for use
    in combining multiple files: the same sequence in multiple files will
    use the same index.

    `format` can be passed explicitly, otherwise auto-detection is attempted.
    """

    parser = BaseParser(filename, fmt, fmt_cols)

    if sequence_indices is None:
        sequence_indices = {}
        samples = {}


    df = pd.read_table(filename)

    # Map column names to ones that can be accessed from Python:
    # df.columns = [c.replace(' ', '_') for c in df.columns]

    for _,row in df.iterrows():
        sample_name = parser.getSample(row)
        if sample_name not in samples:
            samples[sample_name] = {"Sample": sample_name}
        sample = samples[sample_name]

        sequence = parser.getSequence(row)
        if sequence not in sequence_indices:
            sequence_indices[sequence] = len(sequence_indices)
        sequence_idx = sequence_indices[sequence]

        count = parser.getCount(row)
        sample[sequence_idx] = sample.get(sequence_idx, 0) + count

    return sequence_indices, samples
