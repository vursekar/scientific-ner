import bibtexparser
import requests
from pathlib import Path

N = 2000

with open('anthology.bib') as bibtex_file:
    bibtex_str = [next(bibtex_file) for x in range(N)]

bibtex_str = ''.join(bibtex_str)
bib_database = bibtexparser.loads(bibtex_str)

for entry in bib_database.entries:
    print(entry['title'])
    url = entry['url']+'.pdf'
    filename = url.split('/')[-1]
    filepath = Path('scraped_pdfs/{}'.format(filename))
    response = requests.get(url)
    filepath.write_bytes(response.content)
