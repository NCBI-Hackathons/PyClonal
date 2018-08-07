from __future__ import print_function
import os
import sys

import pandas as pd

def detectFileFormat(filename):
    """
    Does a simple auto-detection of file format based on column names.
    """

    first_line = open(filename).readline()

    # Look for an arbitrary subset of column names to detect format:
    detect_columns = {
            "mixcr": ["clonalSequenceQuality", "minQualFR1", "allDAlignments"],
            "changeo": ["SEQUENCE_ID", "JUNCTION_LENGTH", "CLONE_CDR3_AA"],
            "vdjtools": ["frequency", "CDR3nt", "CDR3aa"],
            "immunoseq": ["aminoAcid", "frequencyCount", "cdr3Length"],
            "mitcr": ["Read count", "CDR3 amino acid sequence", "V segments"],
    }

    for type, column_names in detect_columns.items():
        if all([column_name in first_line for column_name in column_names]):
            print("%s looks like a %s file" % (filename, type))
            return type

    raise Exception("Unable to detect format of %s" % filename)

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


class MixcrParser(object):
    def __init__(self, filename):
        self.sample = os.path.basename(filename).rsplit('.', 1)[0]

    def getSample(self, row):
        return self.sample

    def getSequence(self, row):
        return row.aaSeqCDR3

    def getCount(self, row):
        return row.cloneCount

class MitcrParser(object):
    def __init__(self, filename):
        self.sample = os.path.basename(filename).rsplit('.', 1)[0]

    def getSample(self, row):
        return self.sample

    def getSequence(self, row):
        return row.CDR3_amino_acid_sequence

    def getCount(self, row):
        return row.Read_count

class ChangeoParser(object):
    def __init__(self, filename):
        pass

    def getSample(self, row):
        return row.SAMPLE

    def getSequence(self, row):
        return row.CLONE_CDR3_AA

    def getCount(self, row):
        return row.DUPCOUNT

class VDJToolsParser:
    def __init__(self, filename):
        self.sample = os.path.splitext(os.path.basename(f))[0]

    def getSample(self, row):
        return self.sample

    def getSequence(self, row):
        return self.CDR3aa

    def getCount(self, row):
        return self.count

class ImmunoSeqParser:
    def __init__(self, filename):
        self.sample = os.path.splitext(os.path.basename(f))[0]

    def getSample(self, row):
        return self.sample

    def getSequence(self, row):
        return self.aminoAcid

    def getCount(self, row):
        return self.count

PARSERS = {
        'changeo': ChangeoParser,
        'mixcr': MixcrParser,
        'vdjtools': VDJToolsParser,
        'immunoseq': ImmunoSeqParser,
        'mitcr': MitcrParser,
        }


def parseFile(filename, sequence_indices=None, samples=None, format=None):
    """
    Parses a file, returning a sequence_id => count mapping.

    Accumulates the results in `sequence_indices` and `samples` for use
    in combining multiple files: the same sequence in multiple files will
    use the same index.

    `format` can be passed explicitly, otherwise auto-detection is attempted.
    """

    if format is None:
        format = detectFileFormat(filename)

    parser = PARSERS[format](filename)

    if sequence_indices is None:
        sequence_indices = {}
        samples = {}


    df = pd.read_table(filename)

    # Map column names to ones that can be accessed from Python:
    df.columns = [c.replace(' ', '_') for c in df.columns]

    for row in df.itertuples():
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
