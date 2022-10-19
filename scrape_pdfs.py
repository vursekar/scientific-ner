import pandas as pd
import numpy as np
import requests
from pathlib import Path

path_to_csv = 'anthology.csv'
num_files = 50

np.random.seed(0)

acl_df = pd.read_csv(path_to_csv, index_col=0)
acl_df['link_to_pdf'] = acl_df['url'].apply(lambda x: str(x) + '.pdf')
acl_df = acl_df[acl_df.publisher.isin(['Association for Computational Linguistics'])]

idxs = np.random.choice(acl_df.shape[0], num_files, replace=False)
urls = acl_df.iloc[idxs]['link_to_pdf'].values

for url in urls:
    filename = url.split('/')[-1]
    print(filename)
    filepath = Path('scraped_pdfs/{}'.format(filename))
    response = requests.get(url)
    filepath.write_bytes(response.content)
