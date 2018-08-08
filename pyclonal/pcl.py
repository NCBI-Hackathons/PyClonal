#!/usr/bin/env python

import os
import argparse
import glob
from .io import combineFiles, FmtReader

def check_arg_len(kwargs, arg, length):
    if arg in kwargs and not len(kwargs[arg]) in (0, length):
        raise ValueError('{} option requires exactly 3 parameters'.format(arg))


def main():
    parser = argparse.ArgumentParser(description='''
    A Jupyter notebook based framework to analyzi T-cell receptor sequencing
    data.

    Provide an interactive set of Jupyter notebooks for easily visualizing and
    analyzing TCR sequencing data using existing tools and methods.
    '''
    )

    parser.add_argument('dir', type=str, default='.', help='directory with data files')
    parser.add_argument('-p', '--pattern', type=str, default='*.tsv',
            help='filename patterd (*.tsv)')
    parser.add_argument('-f', '--format', nargs='*', type=str,
            help='custom format: names of columns to extract')
    parser.add_argument('-n', '--format_name', type=str,
            help='custom format name')
    parser.add_argument('-c', '--format_cols', nargs='*', type=str,
            help='column to detect format')
    parser.add_argument('-o', '--output_file', type=str, default='output', help='output files basename')

    args = parser.parse_args()
    kwargs = vars(args)
    if kwargs['format'] is None and not kwargs['format_cols'] is None:
        raise ValueError('--format option requires --format_cols option.')
    
    if kwargs['format'] is not None and kwargs['format_name'] is None:
        kwargs['format_name'] = 'custom_fmt'

    if kwargs['format'] is not None:
        check_arg_len(kwargs, 'format', 3)
        check_arg_len(kwargs, 'fotmat_cols', 3)
        fmt = {kwargs['format_name']: kwargs['format']}
        fmt_cols = {kwargs['format_name']: kwargs['format_cols']}
    else:
        fmt = fmt_cols = None

    reader = FmtReader(glob.glob(os.path.join(kwargs['dir'], kwargs['pattern'])), fmt, fmt_cols)
    samples_df, seq_df = reader.process_files()

    samplesout = os.path.join(kwargs['dir'], '{}_samples.csv'.format(kwargs['output_file']))
    seqout = os.path.join(kwargs['dir'], '{}_seq.csv'.format(kwargs['output_file']))

    samples_df.to_csv(samplesout)
    seq_df.to_csv(seqout)
    print("All done. Output written to {} and {}".format(samplesout, seqout))

if __name__ == "__main__":
    main()
