import os
from PyPDF2 import PdfReader
import spacy
import re

pdfs_folder = 'scraped_pdfs/train/'
text_folder = 'tokenized_texts/train/'

filenames = os.listdir(pdfs_folder)
nlp = spacy.load("en_core_web_sm")

for filename in filenames:
    if '.pdf' in filename:
        filetitle = filename[:-4] #remove .pdf extension
        filename = os.path.join(pdfs_folder, filename)
        textfile = os.path.join(text_folder, filetitle+'.txt')

        if os.path.exists(textfile):
            print('skipping since already exists')
            continue

        try:
            reader = PdfReader(filename)
            print("Number of pages = {}".format(len(reader.pages)))
        except:
            print("Error parsing PDF")
            continue

        with open(textfile, 'w') as fout:
            for page in reader.pages:
                text = page.extract_text()
                text = re.sub(r"-+ *\n+ *", "", text)
                text = re.sub("\n", " ", text)

                doc = nlp(text)

                for sent in doc.sents:
                    print(' '.join([token.text for token in sent]), end='\n', file=fout)
