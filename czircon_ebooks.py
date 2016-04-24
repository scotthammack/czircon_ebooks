#!/usr/local/bin/python
# coding: utf-8

import json
import random
import re
import string
import tweepy

from twitter_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, DATABASE

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

OUTPUT_LENGTH = 140
JUMP_PROB = 0.3

def assemble_corpus(database):
	source_file = open(database,'r')
	source = source_file.readlines()
	source_file.close()

	corpus = []

	for line in source:
		for word in line.split():
			corpus.append(word)
	return corpus


def get_start_pos():
	while True:
		pos = random.randint(0, len(corpus) - 1)
		if corpus[pos].istitle():
			return pos

def get_word_pos(target):
	counter = 0
	instances = []

	for word in corpus:
		if strip_punct(word) == target:
			instances.append(counter)
		counter += 1

	if instances:
		return random.choice(instances)
	else:
		return None

def strip_punct(word):
	word = word.lower()
	return word.translate(string.maketrans("",""), string.punctuation)


def create_post(corpus):
	tweet = ''
	wordnum = 0

	position = get_start_pos()

	while len(tweet) < OUTPUT_LENGTH - len(corpus[position]):

		if wordnum == 0:
			new_word = corpus[position].capitalize()
		else:
			new_word = corpus[position]
		tweet += new_word

		wordnum += 1

		if (corpus[position].endswith(('.','?','!','.\"','!\"','?\"')) and corpus[position + 1].istitle() and not corpus[position].endswith(('Mr.','Mrs.', 'Dr.','Ms.'))):
			return tweet

		if random.random() <= JUMP_PROB:
			word_to_look_for = strip_punct(corpus[position + 1])
			position = None
			while not position:
				position = get_word_pos(word_to_look_for)
		else:
			position += 1

		tweet += ' '
	
	return tweet


corpus = assemble_corpus(DATABASE)

output = create_post(corpus)
print output
api.update_status(output)
