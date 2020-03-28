import re
import string
import contractions
from bs4 import BeautifulSoup
from nltk.tokenize import TweetTokenizer

class TextPreprocessor(object):
    def __init__(self):
        pass

    def remove_html(self, text):
        soup = BeautifulSoup(text, 'lxml')
        souped = soup.get_text()
        return souped

    def remove_url(self, text):
        return re.sub(r'http\S+', '', text)

    def remove_mention(self, text):
        return re.sub('@[^\s]+','',text)

    def remove_hashtag(self, text):
        return re.sub(r'#\w*', '', text)

    def remove_punctuation(self, text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def fix_contractions(self, text):
        return contractions.fix(text)

    def process(self, text):
        text = self.remove_html(text)
        text = self.remove_mention(text)
        text = self.remove_url(text)
        text = self.remove_hashtag(text)
        text = self.fix_contractions(text)

        words = TweetTokenizer().tokenize(text)
        words = [word.lower() for word in words]
        # Remove punctuation
        words = [self.remove_punctuation(word) for word in words]
        # Remove words that contain numeric values
        words = [word for word in words if word.isalpha()]
        
        return " ".join(words)