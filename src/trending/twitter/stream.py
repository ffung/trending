# -*- coding: utf-8 -*-

import logging

import tweepy

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"

_logger = logging.getLogger(__name__)


class StreamToFileListener(tweepy.StreamListener):
    def __init__(self, destination_file):
        self.destination_file = destination_file

    def on_data(self, data):
        with open(self.destination_file, 'a') as tf:
            tf.write(data)
        return True

    def on_error(self, data):
        _logger.error("Error occured: %s" % data)
        return False


class TweetStreamer:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def stream_to_file(self, tweet_filter_dict, destination_file):
        stream_listener = StreamToFileListener(destination_file)
        stream = tweepy.Stream(auth=self.api.auth, listener=stream_listener)
        stream.filter(**tweet_filter_dict, is_async=True)

