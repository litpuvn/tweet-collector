import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import os
import arrow
import pytz


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Tweet Downloader")
    parser.add_argument("-k",
                        "--keyword",
                        dest="keywords",
                        help="Keywords to filter",
                        default='harvey')
    parser.add_argument("-s",
                        "--startDate",
                        dest="startDate",
                        help="Minimum date (YYYY-MM-DD) that the tweets were created",
                        default= '2017-08-26')

    parser.add_argument("-e",
                        "--endDate",
                        dest="endDate",
                        help="Maximum date (YYYY-MM-DD) that the tweets were created",
                        default= '2017-09-08')

    parser.add_argument("-o",
                        "--output",
                        dest="output",
                        help="Output folder",
                        default= os.getcwd()
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

    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
    #collecting data
    searchQuery = '#' + args.keywords  # this is what we're searching for
    maxTweets = 100  # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    fName = 'tweets.txt'  # We'll store the tweets in a text file.

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None


    startDate = arrow.get(args.startDate, 'YYYY-MM-DD').replace(tzinfo='local')
    endDate = arrow.get(args.endDate, 'YYYY-MM-DD').replace(tzinfo='local')

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    noMoreTweet = False
    with open(fName, 'w') as f:
        while not noMoreTweet:
            try:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, until=endDate.format('YYYY-MM-DD'))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, until=endDate.format('YYYY-MM-DD'), since_id=sinceId)

                if not new_tweets:
                    print("No more tweets found")
                    noMoreTweet = True
                    break

                for tweet in new_tweets:
                    createdAt = pytz.utc.localize(tweet.created_at)
                    if (createdAt < startDate.datetime):
                        noMoreTweet = True
                        break
                    f.write(json.dumps(tweet._json) + '\n')
                    tweetCount += 1

                print("Downloaded {0} tweets".format(tweetCount))
                sinceId = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                noMoreTweet = True

                break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))