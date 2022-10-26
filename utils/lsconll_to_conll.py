import os
import json
import re

path_to_tagged = 'data/final_dataset/manual/train/'
path_to_output = 'data/final_dataset/manual_formatted/train/'

filenames = os.listdir(path_to_tagged)

if not os.path.exists(path_to_output):
    os.makedirs(path_to_output)

for filename in filenames:

    if '.conll' not in filename:
        continue

    outfilename = filename

    with open(os.path.join(path_to_tagged,filename)) as fin:
        with open(os.path.join(path_to_output, outfilename), 'w') as fout:
            for line in fin:

                try:
                    token, _, _, tag = line.strip().split(' ')
                    fout.write(f'{token}\t{tag}\n')
                except ValueError:
                    try:
                        token, tag = line.strip().split(' ')
                        fout.write(f'{token}\t{tag}\n')
                    except ValueError:
                        fout.write('\n')
