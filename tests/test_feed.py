# -*- coding: utf-8 -*-

import pytest
import re
from unittest.mock import patch, mock_open

from trending.rss.feed import Feed

__author__ = "Fai Fung"
__copyright__ = "Fai Fung"
__license__ = "mit"

def test_generate_feed():
    feed = Feed("www.nu.nl")
    rss = feed.generate(["a", "b", "c"])

    assert rss != None
    expected = """<?xml version='1.0' encoding='UTF-8'?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
  <channel>
    <title>Trending Twitter Feed</title>
    <link>www.nu.nl</link>
    <description>Trending Twitter Feed</description>
    <docs>http://www.rssboard.org/rss-specification</docs>
    <generator>python-feedgen</generator>

    <item>
      <title>c</title>
      <link>www.nu.nl/c</link>
      <description>c</description>
    </item>
    <item>
      <title>b</title>
      <link>www.nu.nl/b</link>
      <description>b</description>
    </item>
    <item>
      <title>a</title>
      <link>www.nu.nl/a</link>
      <description>a</description>
    </item>
  </channel>
</rss>
"""
    rss_without_generation_date = re.sub(
        r".*<lastBuildDate>.*</lastBuildDate>", "", rss.decode())
    assert rss_without_generation_date == expected
