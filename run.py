import tweepy
from tweepy import Stream
# from tweepy import OAuthHandler
from tweepy import AppAuthHandler
from datetime import datetime, timedelta

from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import os
import arrow
import pytz
import os.path

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Tweet Downloader")
    parser.add_argument("-k",
                        "--keyword",
                        dest="keywords",
                        help="Keywords to filter",
                        default='harvey')

    lastSevenDay = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

    parser.add_argument("-s",
                        "--startDate",
                        dest="startDate",
                        help="Minimum date (YYYY-MM-DD) that the tweets were created",
                        default=lastSevenDay)

    parser.add_argument("-e",
                        "--endDate",
                        dest="endDate",
                        help="Maximum date (YYYY-MM-DD) that the tweets were created",
                        default=yesterday)

    parser.add_argument("-o",
                        "--output",
                        dest="output",
                        help="Output folder",
                        default= os.getcwd()
                        )

    parser.add_argument("-p",
                        "--prefix",
                        dest="prefix",
                        help="Output file prefix name",
                        default= ""
                        )
    return parser


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    auth = AppAuthHandler(config.consumer_key, config.consumer_secret)
    #auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    #collecting data
    searchQuery = '#' + args.keywords  # this is what we're searching for
    tweetsPerQry = 100  # this is the max the API permits
    fName = 'tweets.txt'  # We'll store the tweets in a text file.

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    startDate = arrow.get(args.startDate, 'YYYY-MM-DD').replace(tzinfo='local')
    endDate = arrow.get(args.endDate, 'YYYY-MM-DD').replace(tzinfo='local')

    outputPrefix = args.prefix
    rootFolder = args.output + '/' + outputPrefix

    if (outputPrefix and not os.path.isdir(rootFolder)):
        os.makedirs(rootFolder)

    tweetCount = 0
    print("Downloading tweets from {0} to {1} with keyword {2}".format(args.startDate, args.endDate, args.keywords ))
    noMoreTweet = False
    newFile = False
    f = False

    # search until this searchDate but not include the searchDate
    searchDate = startDate + timedelta(days=1)
    new_tweets = False

    while not noMoreTweet:
        try:
            searchDateStr = searchDate.format('YYYY-MM-DD')

            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, until=searchDateStr)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, until=searchDateStr, since_id=sinceId)

            if not new_tweets:
                if (searchDate.datetime <= endDate):
                    searchDate = searchDate + timedelta(days=1)
                    print("Downloading for date {0}".format(searchDate.format('YYYY-MM-DD')))
                    continue

                print("No more tweets found")
                noMoreTweet = True
                break

            for tweet in new_tweets:
                createdAt = pytz.utc.localize(tweet.created_at)
                if (createdAt < startDate.datetime):
                    noMoreTweet = True
                    # ignore tweet that created not in range (startDate to searchDate)
                    # the sinceId is lower bound to avoid getting duplicate tweets when searching tweets in more recent dates
                    break

                fName = outputPrefix + "-" + createdAt.strftime('%Y-%m-%d') + ".json"
                if (not os.path.isfile(fName)):
                    # close previous file
                    if (not f and not isinstance(f, (bool)) and not f.closed):
                        f.close()
                    # open new file name to write
                    f = open(fName, 'w')
                else:
                    # open existing file to write
                    if (not f or f.closed):
                        f = open(fName, 'a')

                f.write(json.dumps(tweet._json) + '\n')
                tweetCount += 1

            print("Downloaded {0} tweets".format(tweetCount))
            sinceId = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            noMoreTweet = True

            if (not f and not f.closed):
                f.close()

            break

    #print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))