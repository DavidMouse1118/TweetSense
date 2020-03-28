from fast_bert.prediction import BertClassificationPredictor
from text_preprocessor import TextPreprocessor

class SentimentAnalyzer(object):
    def __init__(self, model_path, label_path):
        self.predictor = BertClassificationPredictor(
                        model_path=model_path,
                        label_path=label_path, # location for labels.csv file
                        multi_label=False,
                        model_type='bert',
                        do_lower_case=False)
        self.preprocessor = TextPreprocessor()


    def predict_sentiment(self, tweet):
        tweet = self.preprocessor.process(tweet)
        print(tweet)
        prediction = self.predictor.predict(tweet)
        print(prediction)
        for label, confidence in prediction:
            if label == "0" and confidence >= 0.7:
                return "Negative"

            if label == "4" and confidence >= 0.7:
                return "Positive"

        return "Neutral"

    def batch_predict_sentiment(self, tweets):
        processed_tweets = []

        for tweet in tweets:
            processed_tweets.append(self.preprocessor.process(tweet))

        predictions = self.predictor.predict_batch(processed_tweets)
        print(predictions)
        results = []

        for prediction in predictions:
            label_to_prob = dict(prediction)

            if label_to_prob["0"] >= 0.7:
                results.append("Negative")
            elif label_to_prob["4"] >= 0.7:
                results.append("Positive")
            else:
                results.append("Neutral")

        return results
