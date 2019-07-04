# -*- coding: utf-8 -*-

import logging

from feedgen.feed import FeedGenerator

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"

_logger = logging.getLogger(__name__)


class Feed():
    def __init__(self, url):
        self.url = url

    def generate(self, entries):
        fg = FeedGenerator()
        fg.title("Trending Twitter Feed")
        fg.link(href=self.url)
        fg.description("Trending Twitter Feed")

        for entry in entries:
            fe = fg.add_entry()
            fe.title(entry)
            fe.link(href=self.url + "/" + entry)
            fe.description(entry)

        return fg.rss_str(pretty=True)

if __name__ == "__main__":
    run()
