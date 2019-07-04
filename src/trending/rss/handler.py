# -*- coding: utf-8 -*-

import logging

from trending.rss.feed import Feed
from http.server import BaseHTTPRequestHandler, HTTPServer

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class FeedHandler(BaseHTTPRequestHandler):
    def __init__(self, baseurl, hashtags, words, *args, **kwargs):
        self.baseurl = baseurl
        self.hashtags = hashtags
        self.words = words
        super().__init__(*args, **kwargs)

    def do_GET(self):
        feed = Feed(self.baseurl)
        self.send_response(200)

        if self.path == "/hashtags":
            rss = feed.generate(self.hashtags)
        elif self.path == "/words":
            rss = feed.generate(self.words)
        else:
            self.send_response(404)
            return

        self.send_header("Content-type", "application/rss+xml")
        self.end_headers()
        self.wfile.write(rss)

