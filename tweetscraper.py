#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, csv, string

with open('tweets.csv') as tweets:
	tweetreader = csv.reader(tweets)
	for row in tweetreader:
		tweet = row[5]
		if not tweet.startswith('RT') and tweet.find('@') == -1 and string.find(tweet, 'http') == -1:
			print tweet
