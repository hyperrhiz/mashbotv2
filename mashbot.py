#!/usr/bin/python
from __future__ import print_function
import markovify
import tweepy
import random
import datetime
from keys import keys
from unidecode import unidecode
import textwrap
from Adafruit_Thermal import *


# Starts the api and auth
consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Creates the post and logs to a file
def generate_post():
    with open('/home/yuri/mashbotv2/cleaned.txt') as f:
        text = f.read()

    text_model = markovify.Text(text, state_size=2)
    mash_text = text_model.make_short_sentence(129) # was 140
    wrapped_text = textwrap.fill(mash_text, 32)
    output_text = "@acoluthon " + mash_text

    printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
    printer.setDefault()
    printer.justify('L')
    printer.feed(3)
    printer.boldOn()
    printer.setSize('M')
    printer.println("Mash Note")
    printer.setSize('S')
    printer.boldOff()
    printer.println(wrapped_text)
    printer.feed(2)

    # Write the status to a file, for debugging
    with open('/home/yuri/mashbotv2/history.txt', 'a') as f:
        f.write('mashed: ' + mash_text + ' | tweeted: ' + output_text + '\n')

    return output_text

#if not posting to twitter, uncomment to get output
#generate_post()

# Post the status to Twitter
api.update_status(status=generate_post())
