# -*- coding: utf-8 -*-

import logging
from collections import Counter

import pandas as pd
from pandas.io.json import read_json
from pandas.io.json import json_normalize

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class TweetsAnalyzer():
    def __init__(self, tweets_file):
        self.tweets_file = tweets_file

    def trending(self):
        tweets = read_json(self.tweets_file, lines=True)

        top_trending_words = pd.Series(' '.join(tweets.text).lower().split()).value_counts()[:50]

        # get used hashtags per tweet
        hashtags = json_normalize(tweets['entities'], 'hashtags',  errors='ignore')
        hashtags['text'] = hashtags['text'].str.lower()
        top_trending_hashtags = hashtags['text'].value_counts()[:50]

        _logger.debug("top trending words: \n%s" % top_trending_words)
        _logger.debug("top trending hashtags: \n%s" % top_trending_hashtags)
        return (top_trending_hashtags, top_trending_words)

if __name__ == "__main__":
    ta = TweetsAnalyzer("tweets.txt")
    ta.trending()
