# -*- coding: utf-8 -*-

import pytest
from unittest.mock import patch, mock_open

from trending.analysis.tweets import TweetsAnalyzer

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"


def test_tweets_analyzer():
    analyzer = TweetsAnalyzer("tests/test.txt")
    trending = analyzer.trending()
    trending_hashes = trending[0]
    trending_words = trending[1]
    assert trending != None
    assert len(trending_hashes) == 50
    assert len(trending_words) == 50

    assert trending_hashes.index[0] ==  "brugopen"
    assert trending_words.index[0] ==  "in"

