import os
import json
import re

path_to_tagged = 'data/scipdf_tagged/test/'
path_to_output = 'data/final_data/auto/test/'

filenames = os.listdir(path_to_tagged)

if not os.path.exists(path_to_output):
    os.makedirs(path_to_output)

for filename in filenames:

    if '.json' not in filename:
        continue

    outfilename = re.sub('.json', '.conll', filename)

    with open(os.path.join(path_to_tagged,filename)) as fin:
        with open(os.path.join(path_to_output, outfilename), 'w') as fout:
            for sample in fin:
                sample = json.loads(sample)

                text = sample['text'].split(' ')
                entities = ['O' for _ in range(len(text))]

                for start, end, et, word in sample['entities']:
                    entities[start] = 'B-{}'.format(et)

                    for idx in range(start+1, end):
                        entities[idx] = 'I-{}'.format(et)

                for idx in range(len(text)):
                    fout.write(f'{text[idx]}\t{entities[idx]}\n')

                fout.write('\n')
