#!/bin/sh

set -e
aws s3  --region eu-west-1 cp s3://trending-bucket/trending.ini trending.ini
PYTHONPATH=src: python src/trending/main.py
