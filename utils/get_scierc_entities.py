import json
import os

named_entities = {}
directory_path = 'scierc_data/'
path_to_entity_files = 'entity_corpus/'

filenames = os.listdir(directory_path)

for filename in filenames:

    if '.json' not in filename:
        continue

    path = os.path.join(directory_path, filename)

    with open(path) as f:
        for jsonObj in f:
            sample = json.loads(jsonObj)

            paragraph = []

            for sentence in sample['sentences']:
                paragraph += sentence

            for idx, spans in enumerate(sample['ner']):
                for span in spans:
                    named_entities[span[2]] = named_entities.get(span[2], set())
                    named_entities[span[2]].add(' '.join(paragraph[span[0]:span[1]+1]))

for key in named_entities:
    named_entities[key] = list(named_entities[key])


with open(os.path.join(path_to_entity_files, 'scierc_entities.json'), 'w') as f:
    json.dump(named_entities, f)
