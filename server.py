from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, FloatField, TextAreaField, validators, StringField, SubmitField
import os

from twitter_scraper import get_tweets

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
    # print("HERE")
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
    # print("w0", type(wordsets[0]))
    for i in nltk.sent_tokenize(textsets[0]):
        word_ = nltk.word_tokenize(i)
        try:
            start_keys.append(" ".join(word_[:context]))
        except:
            pass
    total_words = sum([len(d) for d in wordsets])
    # Creating mapping, N : N+1th word and store in a dict for
    # both datasets and weight them according to the norm and
    # the given datasets
    # print('hello im here')
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
    # print('heyyyyo')
    # print(start_keys)
    # with open("rule_keys", "w+") as fout:
    #     fout.write(str(rule))
    #     fout.write(str(start_keys))
    return rule, start_keys


def makestring(rule, start_keys, length):
    '''Use a given rule to make a string.'''
    #  Get a starting word randomly
    string = ""
    # print("In makestring")
    boo1 = True
    while boo1:
        # print("Trying to make tweet")
        stringold = string
        string = random.choice(start_keys)+' '
        oldwords = string.split()
        # Iterate till number of sentences are reached
        boo = True
        # print('here the third')
        while length > 0 and boo:
            # print("In inner loop")
            # print(string)
            stringold = string
            # Get new key
            key = ' '.join(oldwords)
            try:
                word_choices = []
                choice_distribution = []
                # Get distributions and words for next choice
                for word_choice, weight in rule[key].items():
                    # print("In loop to get distributions")
                    word_choices.append(word_choice)
                    choice_distribution.append(weight)
                # Normalize the distribution
                choice_distribution = choice_distribution / \
                    np.sum(choice_distribution)
                # Choose word based on distribution
                newword = np.random.choice(word_choices, p=choice_distribution)
                if stringold == (string+newword):
                    boo = False
                    boo1 = True
                    break
                string += newword + ' '
                # Check for ending punctuation
                if "." in newword or "!" in newword or "?" in newword:
                    length -= 1
                # Update oldwords
                if len(string) > 200:
                    boo = False
                for word in range(len(oldwords)):
                    # print("In oldwords loop")
                    oldwords[word] = oldwords[(word + 1) % len(oldwords)]
                oldwords[-1] = newword
            except KeyError:
                boo1 = True
        boo1 = False
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


def run_tweet_generator(tweets, tweet_weight):
    datasets = []
    datasets.append(tweets)
    datasets.append(readdata('test2.txt'))
    weights = [tweet_weight, 1 - tweet_weight]

    rule, start_keys = makerule(datasets, weights, 2)
    tweet = makestring(rule, start_keys, 4)

    return tweet


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

def get_tweet(username, range):
    tweets = '\n'.join([t['text'] for t in get_tweets(username, pages=10)])

    # print(tweets)
    # return "hi"

    return run_tweet_generator(tweets, 1-float(range))

class SetupForm(Form):
    handle = TextField('handle', validators=[validators.required()])
    selectorRange = FloatField('selectorRange', validators=[validators.required()])
    generate = SubmitField('generate')

@app.route("/", methods=['GET', 'POST'])
def index():
    setupForm = SetupForm(request.form)
    # generateForm = GenerateForm(request.form)

    print(setupForm.errors)
    if request.method == 'POST':
        handle = request.form['handle']
        range = request.form['selectorRange']
        print(handle)
        print(range)

        tweet = get_tweet(handle, range)

    if setupForm.validate():
        # Save the comment here.
        flash(handle, 'handleName')
        flash(tweet, 'tweet')
    else:
        flash('ADSA_EOH_2019 ', 'handleName')
        flash("UIUC ADSA tweet generator using markov chains.", 'tweet')

    return render_template('index.html', form=setupForm)

if __name__ == "__main__":
    app.run()
