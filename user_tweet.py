#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import argparse
import os
from tweepy import AppAuthHandler
import config

# Twitter API credentials
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_token
access_secret = config.access_secret

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Tweet Downloader")
    parser.add_argument("-s",
                        "--screenname",
                        dest="screenName",
                        help="Username(s) of a twitter account",
                        default='twdb')

    return parser

def write_tweets_to_file(screen_name, tweets):
    # write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows([tweets])
    pass

def get_all_tweets(screen_name, api):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        #write_tweets_to_file(screen_name, new_tweets)
        # # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    #outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    write_tweets_to_file(screen_name, alltweets)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    screenNameList = args.screenName.split(",")
    
    auth = AppAuthHandler(config.consumer_key, config.consumer_secret)
    # auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # pass in the username of the account you want to download
    for name in screenNameList:
        print "Screen Name: {}".format(name)
        get_all_tweets(name, api)
        print