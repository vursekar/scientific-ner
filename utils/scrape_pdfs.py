import pandas as pd
import numpy as np
import requests
from pathlib import Path
import os

path_to_csv = 'data/anthology.csv'
num_files, num_test_files = 200, 50

np.random.seed(0)

acl_df = pd.read_csv(path_to_csv, index_col=0)
acl_df['link_to_pdf'] = acl_df['url'].apply(lambda x: str(x) + '.pdf')
acl_df = acl_df[acl_df.publisher.isin(['Association for Computational Linguistics'])]

idxs = np.random.choice(acl_df.shape[0], num_files, replace=False)
urls = acl_df.iloc[idxs]['link_to_pdf'].values

test_urls, train_urls = urls[:num_test_files], urls[num_test_files:],

for url in test_urls:
    filename = url.split('/')[-1]
    print(filename)
    filepath = Path('data/scraped_pdfs/test/{}'.format(filename))

    if os.path.exists(filepath):
        print('exists, skipping')
        continue

    response = requests.get(url)
    filepath.write_bytes(response.content)

for url in train_urls:
    filename = url.split('/')[-1]
    print(filename)
    filepath = Path('data/scraped_pdfs/train/{}'.format(filename))

    if os.path.exists(filepath):
        print('exists, skipping')
        continue

    response = requests.get(url)
    filepath.write_bytes(response.content)
