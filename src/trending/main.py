# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = trending.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import configparser
import logging
import sys

from functools import partial
from http.server import HTTPServer

from trending.analysis.tweets import TweetsAnalyzer
from trending.twitter.stream import TweetStreamer
from trending.rss.handler import FeedHandler
from trending import __version__


__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="trending {ver}".format(ver=__version__))
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def get_configuration(config_file="trending.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)

    return config

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting trender")

    config = get_configuration()
    default = config['default']
    tweets_file = default['tweets_file']
    baseurl = default['baseurl']
    twitter = config['twitter']
    consumer_key = twitter['consumer_key']
    consumer_secret = twitter['consumer_secret']
    access_token = twitter['access_token']
    access_token_secret = twitter['access_token_secret']

    stream = TweetStreamer(consumer_key, consumer_secret,
                           access_token, access_token_secret)

    # Amsterdam region
    tweet_filter = {"locations": [4.729242, 52.278174, 5.079162, 52.431064]}
    # stream.stream_to_file(tweet_filter, tweets_file)
    _logger.info("Trender stopped")

    analyzer = TweetsAnalyzer("tweets.txt")
    trending = analyzer.trending()
    hashtags = list(reversed(trending[0].index))
    words = list(reversed(trending[1].index))
    handler = partial(FeedHandler, baseurl, hashtags, words)
    server = HTTPServer(("localhost", 8080), handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
