#!/bin/sh

set -e
aws s3 cp s3://trending-bucket/trending.ini trending.ini
PYTHONPATH=src: python src/trending/main.py
