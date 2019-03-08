# Import libraries.
import sys
import random
import numpy as np
import nltk
import re
import json


def readdata(file):
    '''Read file and return contents.'''
    with open(file) as f:
        contents = f.read()
    return contents


def makerule(data, context):
    '''Make a rule dict for given data.'''
    rule = {}
    # words = nltk.word_tokenize(data)
    words = re.compile("\s").split(data)
    index = context
    print("HERE")
    for word in words[index:]:
        key = ' '.join(words[index-context:index])
        if key not in rule:
            rule[key] = {}

        if word in rule[ke]:
            rule[key][word] += 1
        else:
            rule[key][word] = 1

        index += 1
    return rule


def makerule(textsets, weights, context):
    '''Make a rule dict for given data.'''
    rule = {}
    # words = nltk.word_tokenize(data)
    # Get all words for all the datasets
    wordsets = [d.split() for d in textsets]
    index = context
    # Get all the sentences in both datasets
    sentsets = [nltk.sent_tokenize(d) for d in textsets]
    start_keys = []
    # Extract starting words for all sentences
    for i in sentsets:
        for j in i:
            word_ = nltk.word_tokenize(j)
            try:
                start_keys.append(" ".join(word_[:context]))
            except:
                pass
    total_words = sum([len(d) for d in wordsets])
    # Creating mapping, N : N+1th word and store in a dict for
    # both datasets and weight them according to the norm and
    # the given datasets
    for i, words in enumerate(wordsets):
        norm = total_words / len(words)
        for word in words[index:]:
            key = ' '.join(words[index-context:index])
            if key not in rule:
                rule[key] = {}
            if word in rule[key]:
                rule[key][word] += weights[i] * norm
            else:
                rule[key][word] = weights[i] * norm
            index += 1
    return rule, start_keys


def makestring(rule, start_keys, length):
    '''Use a given rule to make a string.'''
    #  Get a starting word randomly
    string = random.choice(start_keys)+' '
    oldwords = string.split()
    print(oldwords)
    # Iterate till number of sentences are reached
    while length > 0:
        try:
            # Get new key
            key = ' '.join(oldwords)
            word_choices = []
            choice_distribution = []
            # Get distributions and words for next choice
            for word_choice, weight in rule[key].items():
                word_choices.append(word_choice)
                choice_distribution.append(weight)
            # Normalize the distribution
            choice_distribution = choice_distribution / \
                np.sum(choice_distribution)
            # Choose word based on distribution
            newword = np.random.choice(word_choices, p=choice_distribution)
            string += newword + ' '
            # Check for ending punctuation
            if "." in newword or "!" in newword or "?" in newword:
                length -= 1
            # Update oldwords
            for word in range(len(oldwords)):
                oldwords[word] = oldwords[(word + 1) % len(oldwords)]
            oldwords[-1] = newword
        except KeyError:
            return string
    return string


def _parse_input(json_fi):
    datasets = []
    weights = []
    with open(json_fi) as fn:
        text = json.load(fn)
        for k, v in text.items():
            datasets.append(readdata(v['fi_name']))
            weights.append(v['weight'])

        weights = [w / sum(weights) for w in weights]

    return datasets, weights


if __name__ == '__main__':
    datasets, weights = _parse_input(sys.argv[1])  # json fi name
    rule, start_keys = makerule(datasets, weights, int(
        sys.argv[2]))  # context ( no of words in a chain)
    string = makestring(rule, start_keys, int(
        sys.argv[3]))  # length of sentence
    print(string)
