import markovify
from twitter_scraper import get_tweets
import time

from markov import run_tweet_generator

start = time.time()
print("getting tweets", start)
tweets = '\n'.join([t['text']
                    for t in get_tweets('elonmusk', pages=10)])
# with open('abcd.log', "w+") as fout:
#     fout.write(str(tweets))
print("finished getting tweets", time.time() - start)
# print(tweets)
# text_model = markovify.Text(tweets)
#
# print(text_model.make_short_sentence(280))
a = (run_tweet_generator(tweets, 1))
print(a)
