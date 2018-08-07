from __future__ import print_function
import os
import sys

import pandas as pd

FORMATS = {
        'mixcr': ('cloneCount', 'aaSeqCDR3', None),
        'changeo': ('DUPCOUNT', 'CLONE_CDR3_AA', 'SAMPLE'),
        'vdjtools': ('count', 'cdr3aa', None),
        'mitcr': ('Read_count', 'CDR3_amino_acid_sequence', None),
        'immunoseq': ('count (templates/reads)', 'aminoAcid', None)
        }


FMT_COLS = {
        "mixcr": ["clonalSequenceQuality", "minQualFR1", "allDAlignments"],
        "changeo": ["SEQUENCE_ID", "JUNCTION_LENGTH", "CLONE_CDR3_AA"],
        "vdjtools": ["freq", "cdr3nt", "cdr3aa"],
        "immunoseq": ["aminoAcid", "frequencyCount", "cdr3Length"],
        "mitcr": ["Read count", "CDR3 amino acid sequence", "V segments"],
        }


class BaseParser:
    def __init__(self, filename, fmt=None, fmt_cols=None):
        '''
        Sample format parser.
        Users can provide their custom formats.
        '''

        self.FORMATS = FORMATS
        if fmt is not None:
            self.FORMATS.update(fmt)
        self.FMT_COLS = FMT_COLS
        if fmt_cols is not None:
            self.FMT_COLS.update(fmt_cols)

        fmt = self._detect_format(filename)
        self._filename = filename
        self.cnt_field, self.cdr3_field, self.sample = self._get_field_names(fmt)

    def _detect_format(self, filename):
        """
        Does a simple auto-detection of file format based on column names.
        """

        with open(filename, 'rt') as fh:
            first_line = next(fh)

        for fmt, column_names in self.FMT_COLS.items():
            if all([column_name in first_line for column_name in column_names]):
                print("%s looks like a %s file" % (filename, fmt))
                return fmt

        raise Exception("Unable to detect format of %s" % filename)

    def _get_field_names(self, fmt):
        return self.FORMATS[fmt]

    def getSample(self, row):
        if self.sample is None:
            return os.path.splitext(os.path.basename(self._filename))[0]
        return row[self.sample]


    def getSequence(self, row):
        return row[self.cdr3_field]

    def getCount(self, row):
        return row[self.cnt_field]

def combineFiles(filenames):
    """
    Given a list of filenames, read and parse all of them.

    Returns: two dataframes, a samples dataframe and a sequences dataframe.

    The samples dataframe has one row per sample, and one column per unique clone.
    The sequences dataframe has one row per clone, mapping clone index to clone sequence.
    """

    sequence_indices = {}
    samples = {}

    for filename in filenames:
        parseFile(filename, sequence_indices, samples)

    samples = sorted(samples.items())
    samples_df = pd.DataFrame([p[1] for p in samples])
    samples_df = samples_df.set_index("Sample").fillna(0)

    sequences_df = pd.DataFrame(
            sorted([(v, k) for (k, v) in sequence_indices.items()]),
            columns=["Index", "Sequence"])
    sequences_df = sequences_df.set_index("Index")

    return samples_df, sequences_df


def parseFile(filename, sequence_indices=None, samples=None, format=None):
    """
    Parses a file, returning a sequence_id => count mapping.

    Accumulates the results in `sequence_indices` and `samples` for use
    in combining multiple files: the same sequence in multiple files will
    use the same index.

    `format` can be passed explicitly, otherwise auto-detection is attempted.
    """

    parser = BaseParser(filename)

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

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python %s FILES+" % sys.argv[0])
        sys.exit(1)

    samples_df, sequences_df = combineFiles(sys.argv[1:])

    print(samples_df)

    samples_df.to_csv("samples.tsv", sep="\t")
    sequences_df.to_csv("sequences.tsv", sep="\t")
