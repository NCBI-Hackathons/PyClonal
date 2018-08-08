import os

import pandas as pd

from pyclonal import io

def test_format_detect():
    pass

def runTests():
    samples, sequences = io.combineFiles(os.path.join(os.path.dirname(__file__), "input_test_data"), pattern="*.tsv")

    expected_samples = pd.read_table(os.path.join(os.path.dirname(__file__), "input_test_expected_samples.tsv"))
    expected_samples = expected_samples.set_index("Sample")
    expected_samples.columns = map(int, expected_samples.columns)

    expected_sequences = pd.read_table(os.path.join(os.path.dirname(__file__), "input_test_expected_sequences.tsv"))
    expected_sequences = expected_sequences.set_index("Index")

    assert (samples == expected_samples).all().all(), (samples, expected_samples)
    assert (sequences == expected_sequences).all().all(), (sequences, expected_sequences)


if __name__ == "__main__":
    runTests()
