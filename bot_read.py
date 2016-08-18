#!/usr/bin/python

# with the help of http://pythonforengineers.com/

import praw
import re
import os
from flask import Flask
#from config_bot import * no need for heroku version

app = Flask(__name__) 

r = praw.Reddit(user_agent='bot 0.1 by /u/poupipoupipoupipou')
r.login(os.environ['REDDIT_USERNAME'],  os.environ['REDDIT_PASS'])


key_word = 'thankfulbot'
s = ''
authorList = []
first = True

class SavedSet(set):
	_filename = "posts_replied_to.txt"

	def load_from_file(self):
		with open(_filename, "r") as f:
			return set(f.read().split())

	def add(self, what):
		with open(_filename, "a") as f:
			f.write(what + "\n")
		return super(PostsDone, self).add(what)


def bot_action(c, posts_replied_to, verbose=True, respond=True):
	global first
	global s
	global authorList

	submission = r.get_submission(url=c.link_url)
	if submission.id not in posts_replied_to:
		authorCom = str(c.author)
		authorPost = str(c.link_author)
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		for comment in flat_comments:
			if comment.author.name not in authorList + [authorCom, authorPost]:
				if not first:
					s += ', '
				s += '/u/' + str(comment.author.name)
				authorList.append(comment.author.name)
				first = False
		response = ' I\'m a lazy bot. Thank you ' + s
		if len(authorList) > 1:
			response += ' for your kind answers !'
		else:
			response += ' for your kind answer !'
		print(response)
		c.reply(response)
		posts_replied_to.add(submission.id)


def main():
	for c in praw.helpers.comment_stream(r, 'all'):
		posts = SavedSet()
		if re.search(key_word, c.body, re.IGNORECASE):
			print(vars(c))
			bot_action(c, posts)


if __name__ == '__main__':
	from os import environ
    app.run(debug=False, port=environ.get("PORT", 5000))
	main()
