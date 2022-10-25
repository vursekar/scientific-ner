import os
import spacy
import re

from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader

pdfs_folder = 'scraped_pdfs/test/'
text_folder = 'tokenized_texts/test/'

filenames = os.listdir(pdfs_folder)
nlp = spacy.load("en_core_web_sm")

for filename in filenames:
    if '.pdf' in filename:
        filetitle = filename[:-4] #remove .pdf extension
        filename = os.path.join(pdfs_folder, filename)
        textfile = os.path.join(text_folder, filetitle+'.txt')

        print(filename)

        if os.path.exists(textfile):
            print('skipping since already exists')
            continue

        try:
            text = extract_text(filename)
            text = re.sub(r"-+ *\n+ *", "", text)
            text = text.split('\n\n')

            for subtext in text:
                if len(subtext)>100 and ' ' not in subtext:
                    raise RuntimeError('PDFMiner broken')
                    break

            sents = []

            with open(textfile, 'w') as fout:

                for subtext in text:
                    subtext = re.sub("\n", " ", subtext)
                    subtext = re.sub("et al.", "et al", subtext)
                    subtext = subtext.strip()

                    if subtext in ['References', 'Acknowledgements']:
                        break

                    if len(sents)>0 and len(sents[-1])>40 and len(subtext)>40:
                        sents[-1] = sents[-1] + ' ' + subtext
                    else:
                        sents.append(subtext)

                    doc = nlp(subtext)
                    for sent in doc.sents:
                        print(' '.join([token.text for token in sent]), end='\n', file=fout)

        except:
            print("PDFMiner Failed; trying PyPDF")
            try:
                reader = PdfReader(filename)
                print("Number of pages = {}".format(len(reader.pages)))

                with open(textfile, 'w') as fout:
                    for page in reader.pages:
                        text = page.extract_text()
                        text = re.sub(r"-+ *\n+ *", "", text)
                        text = re.sub("\n", " ", text)

                        doc = nlp(text)

                        for sent in doc.sents:
                            print(' '.join([token.text for token in sent]), end='\n', file=fout)

            except:
                print("Error parsing PDF")
                continue
