import tweepy
import logging
logging.basicConfig(level=logging.INFO)

from tweet_kf_producer import TweetProducer

class TweetHandler(object):
    def __init__(self, 
                 consumer_key, 
                 consumer_secret,
                 access_token,
                 access_secret):

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def stream_tweets(self, key_word, producer):
        stream = tweepy.Stream(auth=self.api.auth, listener=producer)
        stream.filter(track=[key_word], languages = ['en'])

    def get_tweet_text(self, tweet_data):
        if hasattr(tweet_data, "retweeted_status") is True:
            tweet_data = tweet_data.retweeted_status

        if tweet_data.truncated == True:
            return tweet_data.extended_tweet.full_text
        else:
            return tweet_data.full_text

    def get_history_tweets(self, word, count):
        tweets = []
        counter = 0

        for tweet in tweepy.Cursor(self.api.search,
                                   q=word,
                                   lang="en", 
                                   tweet_mode='extended').items():
                                
            tweets.append(self.get_tweet_text(tweet))
            counter += 1
            if counter == count:
                break

        return tweets

    def get_history_tweets_by_dates(self, word, from_date, to_date):
        tweets = []

        for tweet in tweepy.Cursor(self.api.search,
                                   q="{} since:{} until:{}".format(word, from_date, to_date),
                                   lang="en", 
                                   tweet_mode='extended').items():
                            
            tweets.append(self.get_tweet_text(tweet))

        return tweets