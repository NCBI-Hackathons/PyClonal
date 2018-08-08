from __future__ import print_function
import os
import sys

import pandas as pd

FORMATS = {
        'mixcr': ('cloneCount', 'aaSeqCDR3', None),
        'changeo': ('DUPCOUNT', 'CLONE_CDR3_AA', 'SAMPLE'),
        'changeof': ('DUPCOUNT', 'CLONE_CDR3_AA', None),
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
