# -*- coding: utf-8 -*-

import pytest
from unittest.mock import patch, mock_open

from trending.twitter.stream import StreamToFileListener
from trending.twitter.stream import TweetStreamer

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"


def test_stream_listener_on_data():
    listener = StreamToFileListener("test")
    with patch("builtins.open", mock_open()) as mock_file:
        listener.on_data("data")
        mock_file.assert_called_with("test", "a")
        mock_file().write.assert_called_with("data")

@patch("trending.twitter.stream._logger")
def test_stream_listener_on_error(log_mock):
    listener = StreamToFileListener("test")
    assert not listener.on_error("error")
    log_mock.error.assert_called_with("Error occured: error")

@patch("trending.twitter.stream.StreamToFileListener")
@patch("trending.twitter.stream.tweepy")
def test_tweet_streamer(tweepy_mock, listener_mock):
    tweet_streamer = TweetStreamer("consumer_key", "consumer_secret",
                             "access_token", "access_token_secret")
    tweepy_mock.OAuthHandler.assert_called_with(
        "consumer_key", "consumer_secret")
    tweepy_mock.OAuthHandler.return_value.\
        set_access_token.assert_called_with(
        "access_token", "access_token_secret")
    tweepy_mock.API.assert_called_with(
        tweepy_mock.OAuthHandler.return_value)

    tweet_streamer.stream_to_file({"some": "filter"}, "dest")
    tweepy_mock.Stream.assert_called_with(
        auth=tweepy_mock.API.return_value.auth,
        listener=listener_mock.return_value)
    tweepy_mock.Stream.return_value.filter.assert_called_with(
        some="filter", is_async=True)
