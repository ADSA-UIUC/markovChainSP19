from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, FloatField, TextAreaField, validators, StringField, SubmitField
import os

from twitter_scraper import get_tweets
# from markov import run_tweet_generator
import markov

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

def get_tweet(username, range):
    tweets = '\n'.join([t['text'] for t in get_tweets(username, pages=2)])

    print(tweets)

    return run_tweet_generator(tweets, 1-range)

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
