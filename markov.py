#Import libraries.
import sys
import random
import numpy as np
import nltk
import re, json

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

    for word in words[index:]:
        key = ' '.join(words[index-context:index])
        if key not in rule:
            rule[key] = {}

        if word in rule[key]:
            rule[key][word] += 1
        else:
            rule[key][word] = 1

        index += 1

    return rule

def makerule(textsets, weights, context):
    '''Make a rule dict for given data.'''
    rule = {}
    # words = nltk.word_tokenize(data)
    wordsets = [d.split() for d in textsets]

    index = context

    total_words = sum([len(d) for d in wordsets])

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

    return rule

def makestring(rule, length):
    '''Use a given rule to make a string.'''
    oldwords = random.choice(list(rule.keys())).split(' ') #random starting words
    string = ' '.join(oldwords) + ' '

    for i in range(length):
        try:
            key = ' '.join(oldwords)

            word_choices = []
            choice_distribution = []
            for word_choice, weight in rule[key].items():
                word_choices.append(word_choice)
                choice_distribution.append(weight)

            choice_distribution = choice_distribution / np.sum(choice_distribution)
            newword = np.random.choice(word_choices, p=choice_distribution)
            string += newword + ' '

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
    datasets, weights = _parse_input(sys.argv[1]) # json fi name
    rule = makerule(datasets, weights, int(sys.argv[2])) # context
    string = makestring(rule, int(sys.argv[3])) #length
    print(string)
