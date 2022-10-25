import os
import scipdf
import json
from tqdm import tqdm

path_to_pdfs = 'data/scraped_pdfs/train/'
path_to_output = 'data/parsed_pdfs/train/'
filenames = os.listdir(path_to_pdfs)

for i in tqdm(range(len(filenames))):

    filename = filenames[i]

    if '.pdf' not in filename:
        continue

    path = os.path.join(path_to_pdfs, filename)

    try:
        article_dict = scipdf.parse_pdf_to_dict(path)

        with open(os.path.join(path_to_output, filename[:-4] + '.json'), 'w') as f:
            json.dump(article_dict, f)
    except:
        print("Failed to parse")
        continue
