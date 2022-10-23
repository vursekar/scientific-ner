import os
import re
import json
import spacy
from tqdm import tqdm

parsed_text_folder = 'parsed_test_pdfs/'
output_folder = 'scipdf_tokenized/test/'
filenames = os.listdir(parsed_text_folder)
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    text = text.strip()
    text = re.sub('et al.', 'et al ', text)
    text = re.sub('[⊙•→⊕←∈∞§∅∃∧]', ' ', text)
    text = re.sub('[({})\[\];,|-]',' \g<0> ', text)
    text = re.sub(' +', ' ', text)
    text = re.sub('\n+', '\n', text)
    return text

def tokenize_and_write(text, fout, nlp):
    doc = nlp(text)
    for sent in doc.sents:
        line = [re.sub('[\n\t ]',' ',token.text.strip()) for token in sent]

        if len(line)>0:
            line = ' '.join(line)
            line = re.sub(' +', ' ', line)
            if len(line)>0:
                print(line, end='\n', file=fout)

for i in tqdm(range(len(filenames))):

    if '.json' not in filenames[i]:
        continue

    input_filename = os.path.join(parsed_text_folder, filenames[i])

    try:
        with open(input_filename) as f:
            data = f.read()
            data = json.loads(data)

        with open(os.path.join(output_folder, filenames[i][:-5] + '.txt'), 'w') as fout:

            text = preprocess_text(data['title'])
            tokenize_and_write(text, fout, nlp)

            text = preprocess_text(data['abstract'])
            tokenize_and_write(text, fout, nlp)

            for section in data['sections']:
                text = preprocess_text(section['text'])
                tokenize_and_write(text, fout, nlp)

    except:
        print("Error tokenizing {}".format(input_filename))
