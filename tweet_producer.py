import pykafka
import tweepy
import json
import logging
logging.basicConfig(level=logging.INFO)


class TweetProducer(tweepy.StreamListener):
    def __init__(self, broker, topic):
        self.client = pykafka.KafkaClient(broker)
        self.producer = self.client.topics[bytes(topic, "ascii")].get_producer()
        logging.info("Producing tweet into topic {} ...".format(topic))

    def _get_tweet_text(self, tweet_data):
        if tweet_data["truncated"] == True:
            return tweet_data["extended_tweet"]["full_text"]
        else:
            return tweet_data["text"]

    def on_data(self, data):
        data = json.loads(data)

        if isinstance(data, list) == False:
            data = [data]

        for tweet_data in data:
            if "retweeted_status" in tweet_data:
                tweet_data = tweet_data["retweeted_status"]

            tweet_text = self._get_tweet_text(tweet_data)
            tweet_text = tweet_text.encode('ascii', 'ignore').decode('ascii')
            self.producer.produce(bytes(tweet_text, "ascii"))
            
        return True

    def on_error(self, status):
        logging.info("An error happended with status {}.".format(status))
        return True


def main():
    config = json.load(open('config.json'))
    twitter_config = config["twitter"]
    kafka_config = config["kafka"]
    
    # Create Auth object
    auth = tweepy.OAuthHandler(twitter_config["consumer_key"], twitter_config["consumer_secret"])
    auth.set_access_token(twitter_config["access_token"], twitter_config["access_secret"])
    api = tweepy.API(auth)

    # Create stream and bind the TweetProducer to it
    stream = tweepy.Stream(auth, listener = TweetProducer(kafka_config["broker"], kafka_config["input_topic"]))
    stream.filter(track=["Bloomberg"], languages = ['en'])


if __name__ == "__main__":
    main()