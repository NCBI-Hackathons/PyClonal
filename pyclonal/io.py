import os
import glob
import pandas as pd
from .parser import BaseParser

class FmtReader:
    '''
    Handles reading the data from a list of files (of possibly different
    formats. Format specification can be either provided as a list of 
    columns to extract data from (`fmt`)  along with the columns that
    define the format (`fmt_cols`) or detected from the file.
    '''
    def __init__(self, filenames, fmt=None, fmt_cols=None):
        self.filenames = filenames
        self.fmt = fmt
        self.fmt_cols = fmt_cols

    def _detect_delim(self, filename):
        '''
        Simple auto-detection of deilimiter.
        '''
        # ext = os.path.splitext(filename)[1].lower()
        # if ext == '.csv':
        #     return ','
        # else:
        #     return '\t'
        with open(filename, 'rt') as fh:
            header = next(fh)

        if len(header.strip().split(',')) > 3:
            return ','
        elif len(header.strip().split('\t')) > 3:
            return '\t'
        else:
            raise Exception("Unknown delimiter for file {}".format(filename))
    
    def process_files(self):
        """
        Given a list of filenames, read and parse all of them.

        Returns: two dataframes, a samples dataframe and a sequences dataframe.

        The samples dataframe has one row per sample, and one column per unique clone.
        The sequences dataframe has one row per clone, mapping clone index to clone sequence.
        """

        sequence_indices = {}
        samples = {}

        for filename in self.filenames:
            self.parse_file(filename, sequence_indices, samples)

        samples = sorted(samples.items())
        samples_df = pd.DataFrame([p[1] for p in samples])
        samples_df = samples_df.set_index("Sample").fillna(0)

        sequences_df = pd.DataFrame(
                sorted([(v, k) for (k, v) in sequence_indices.items()]),
                columns=["Index", "Sequence"])
        sequences_df = sequences_df.set_index("Index")

        return samples_df, sequences_df


    def parse_file(self, filename, sequence_indices=None, samples=None):
        """
        Parses a file, returning a sequence_id => count mapping.

        Accumulates the results in `sequence_indices` and `samples` for use
        in combining multiple files: the same sequence in multiple files will
        use the same index.

        `format` can be passed explicitly, otherwise auto-detection is attempted.
        """

        parser = BaseParser(filename, self.fmt, self.fmt_cols)

        if sequence_indices is None:
            sequence_indices = {}
            samples = {}

        df = pd.read_table(filename, sep=self._detect_delim(filename))

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

def combineFiles(datadir, pattern=None, fmt=None, fmt_cols=None):
    if pattern is None:
        pattern = '*.tsv'
    filenames = sorted(glob.glob(os.path.join(datadir, pattern)))
    reader = FmtReader(filenames, fmt, fmt_cols)
    return reader.process_files()
