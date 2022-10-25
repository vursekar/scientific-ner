import bibtexparser
import pandas as pd
from pathlib import Path


def bib_to_df(path_to_bib, N):

    with open(path_to_bib) as bibtex_file:
        bibtex_str = [next(bibtex_file) for x in range(N)]

    bibtex_str = ''.join(bibtex_str)
    bib_database = bibtexparser.loads(bibtex_str)
    df = pd.DataFrame.from_records(bib_database.entries)
    return df


if __name__ == "__main__":

    N = 500000 # number of lines to read from bib file
    path_to_bib = 'data/anthology.bib'
    path_to_csv = 'data/anthology.csv'

    df = bib_to_df(path_to_bib, N)
    df.to_csv(path_to_csv)
