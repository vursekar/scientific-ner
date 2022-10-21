import spacy
from spacy.matcher import PhraseMatcher
import json
import os


path_to_tokenized = 'tokenized_texts/'
path_to_tagged = 'tagged_texts/'
filenames = os.listdir(path_to_tokenized)

with open('entity_corpus/pwc_entities.json') as f:
    entity_type_map = json.load(f)

hp_names = ['number of layers', 'number of units', 'activation function', 'L2 regularization', 'epoch number',
            'number of timesteps', 'lrdecay', 'Trainingepochs', 'history size', 'buffer size', 'buffer length',
            'history length', 'context size', 'context length', 'optimizer', 'attention size', 'attention layers',
            'L1 regularization', 'beta', 'alpha', 'learning rate', 'padding size', 'hidden layer size',
            'hidden dimension size', 'embedding dimension', 'word embedding dimension', 'word embedding size',
            'number of epochs', 'minibatch size', 'mini - batch size' , 'size of minibatch', 'number of samples', 'distance metric',
            'learning rate decay rate', 'decay rate', 'weight decay rate', 'batch size', 'momentum term', 'early stopping criterion',
            'θ', 'gamma', 'γ', 'α', 'β', 'δ', 'number of batches', 'number of iterations', 'K =',
            'attention function', 'activaton gate', 'classification threshold', 'number of parameters', 'parameter dimension',
            'number of parameters per layer', 'step size', 'step length', 'epsilon', 'ε', 'eps',
            'max depth', 'maximum depth', 'kernel size', 'kernel dimension', 'number of estimators', 'number of workers']

entity_type_map['HyperparameterName'] = hp_names

nlp = spacy.load("en_core_web_sm")
case_insensitive_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
case_sensitive_matcher = PhraseMatcher(nlp.vocab)

common_vocab = set(nlp.vocab.strings)

entity_type_map_cased = {}
entity_type_map_uncased = {}

for entity_type in entity_type_map:

    entity_type_map_cased[entity_type] = []
    entity_type_map_uncased[entity_type] = []

    for term in entity_type_map[entity_type]:

        if term.lower() in common_vocab:
            entity_type_map_cased[entity_type].append(term)
        else:
            entity_type_map_uncased[entity_type].append(term)

for entity_type in entity_type_map_uncased:
    patterns = [nlp.make_doc(term) for term in entity_type_map_uncased[entity_type]]
    case_insensitive_matcher.add(entity_type, patterns)

for entity_type in entity_type_map_cased:
    patterns = [nlp.make_doc(term) for term in entity_type_map_cased[entity_type]]
    case_sensitive_matcher.add(entity_type, patterns)


for filename in filenames:

    if '.txt' not in filename:
        continue

    print(filename)

    data = []

    with open(os.path.join(path_to_tokenized,filename)) as f:
        sentences = []
        for line in f:
            line = line.strip()
            sentences.append(line)

    with open(os.path.join(path_to_tagged,filename[:-4]+'.json'), 'w') as f:
        for sentence in sentences:
            doc = nlp(sentence)
            matches = case_insensitive_matcher(doc, as_spans=True) + case_sensitive_matcher(doc, as_spans=True)
            matches = [(span.start, span.end, span.label_, span.text) for span in spacy.util.filter_spans(matches)]

            sample = {'text': sentence, 'entities': matches}
            data.append(sample)

        json.dump(data, f)
