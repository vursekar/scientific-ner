# scientific-ner

Initial scratch code to fetch PDFs and obtain tokenized data

1. anthology.bib.gz : Zipped file containing all ACL papers details (with URLs)
2. parse_bib.py : Parses bib file; fetches and saves PDFs for each citation (need to specify how many lines to read)
3. parse_pdfs.py : Parses PDF, tokenizes using Spacy, and saves tokenized PDFs to txt files
