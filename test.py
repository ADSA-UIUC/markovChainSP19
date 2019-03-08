import markovify
from twitter_scraper import get_tweets
import time

start = time.time()
print("getting tweets", start)
tweets = '\n'.join([t['text'] for t in get_tweets('realDonaldTrump', pages=15)])
# print(tweets)
print("finished getting tweets", time.time() - start)
text_model = markovify.Text(tweets)

print(text_model.make_short_sentence(280))
