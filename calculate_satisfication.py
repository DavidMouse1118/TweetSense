from collections import defaultdict
import pandas as pd
from sentiment_analyzer import SentimentAnalyzer

def main():
    tweets = pd.read_csv('tweets.csv')

    LABEL_PATH = "labels/"
    MODEL_PATH = "model/"

    analyzer = SentimentAnalyzer(MODEL_PATH, LABEL_PATH)

    data = defaultdict(lambda: defaultdict(int))
    universities = tweets.iloc[:, 0]
    tweets_text = tweets.iloc[:, 1]

    print("Predicting sentiments...")
    sentiments = analyzer.batch_predict_sentiment(tweets_text)

    for i in range(len(universities)):
        univeristy = universities[i]
        sentiment = sentiments[i]

        data[univeristy][sentiment] += 1

    print(data)

    # calculate the ratio of pos/neg
    university_ratio_posneg = []
    for univeristy in data:
        pos_neg_ratio = data[univeristy]["Positive"] / data[univeristy]["Negative"]
        university_ratio_posneg.append((univeristy, pos_neg_ratio))

    university_ratio_posneg.sort(key=lambda x: x[1], reverse=True)

    for univeristy, pos_neg_ratio in university_ratio_posneg:
        print(univeristy, pos_neg_ratio)

if __name__ == "__main__":
    main()