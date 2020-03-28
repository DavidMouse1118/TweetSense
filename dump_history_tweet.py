import json
from tweet_handler import TweetHandler
import pandas as pd
import time

def main():
    config = json.load(open('config.json'))
    twitter_config = config["twitter"]
    # kafka_config = config["kafka"]
    
    # Create tweet_handler
    tweet_handler = TweetHandler(**twitter_config)

    # Create tweet_producer
    # producer = TweetProducer(kafka_config["broker"], kafka_config["input_topic"])
    # tweet_handler.stream_tweets("bloomberg", producer)

    universities = json.load(open('universities.json'))

    dataframe = pd.DataFrame(columns=['university', 'tweet'])

    for university, hashtag in list(universities.items()):
        # Get history tweets
        history_tweets = tweet_handler.get_history_tweets_by_dates(hashtag, "2020-01-01", "2020-03-25")
        print(len(history_tweets))

        new_df = pd.concat([
            (pd.DataFrame([university] * len(history_tweets))),
            pd.DataFrame(history_tweets)
            ],
            axis=1
        )

        if dataframe.empty:
            dataframe = new_df
        else:
            dataframe = pd.concat([dataframe, new_df], ignore_index=True)

        dataframe.to_csv('tweets.csv', index=False)

        # This line is important - else error 429
        print("Completed {}, sleeping for 15 minutes.".format(university))
        time.sleep(15 * 60)

if __name__ == "__main__":
    main()