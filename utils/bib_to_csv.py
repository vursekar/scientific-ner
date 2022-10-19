import bibtexparser
from pathlib import Path
import pandas as pd

# define number of lines to read from bib file
N = 500000
path_to_bib = 'anthology.bib'

with open(path_to_bib) as bibtex_file:
    bibtex_str = [next(bibtex_file) for x in range(N)]

bibtex_str = ''.join(bibtex_str)
bib_database = bibtexparser.loads(bibtex_str)
df = pd.DataFrame.from_records(bib_database.entries)
df.to_csv('anthology.csv')
