# -*- coding: utf-8 -*-

import logging

from pandas.io.json import read_json

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class TweetsAnalyzer():
    def __init__(self, tweets_file):
        self.tweets_file = tweets_file

    def run(self):
        pd = read_json(self.tweets_file, lines=True)
        print (pd)



if __name__ == "__main__":
    ta = TweetsAnalyzer("tweets.txt")
    ta.run()
