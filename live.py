#!/usr/bin/env python
import os
import sys
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime
import argparse
import config

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-ln",
                        "--lang",
                        dest="language",
                        help="Language",
                        default="en")
    parser.add_argument("-c",
                        "--country",
                        dest="country",
                        help="Country/Alpha-2 Coding (US, UK, MX, ..)",
                        default="US")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data",
                        help="Output/Data Directory",
                        default= str(os.getcwd() + "/data")
                        )
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""
    curDir = ""
    fileNumber = 0
    currentDay = datetime.date.today().strftime('%m-%d-%y')
    tweetCount = 0
    timer = 60 * 30 #60 * N Minutes inbetween message updates
    MAX_SIZE = 1000000000 # 1GB = 1000000000 Max File Size
    endTime = 0

    flushTimer = 60 * 20 #60 * N Minutes (60 * 20 = 20 Minutes)
    flushEnd = 0

    def __init__(self, data_dir):
        #File naming initializers
        self.curDir = data_dir
        self.set_file_name(self.curDir)
        
        #Timer intializers for console updates
        self.timer_check()
        self.flush_file()
        
        print("Listening for Tweets...\nStream updates every {} minutes.\nStart Time: {}".format(int(self.timer/60), datetime.datetime.now()))

    def on_data(self, data):
        try:
            self.set_file_name(self.curDir)
            with open(self.outfile, 'a') as f:
                f.write(data)
                self.tweetCount = self.tweetCount + 1
                self.timer_check()
                self.flush_file()
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(self.curDir)
        if(status == 401):
            print("401 - Unauthorized: Missing or incorrect authentication credentials. This may also returned in other undefined circumstances.")
        elif(status == 400):
            print("400 - Bad Request: The request was invalid or cannot be otherwise served. An accompanying error message will explain further. Requests without authentication are considered invalid and will yield this response.")
        elif(status == 403):
            print("403 - Forbidden: The request is understood, but it has been refused or access is not allowed. An accompanying error message will explain why. This code is used when requests are being denied due to update limits .")
        elif(status == 429):
            print("429 - Too Many Requests: Returned when a request cannot be served due to the applications rate limit having been exhausted for the resource.")
        else:
            print("Error Code: " + status + ", check README for link to all the codes.")
        return True
    
    '''
    Sets the output file that the stream will be write to.
    
    1. If it's a different day, create new file when right date.
    2. Else, check if file exist
        1. If TRUE, check if file size is greater than 1GB
            1. If TRUE, increase the fileCount of that day
        2. Else, use current day and current file count
    '''
    def set_file_name(self, data_dir):
        
        if(self.currentDay != datetime.date.today().strftime('%m-%d-%y')):
            self.currentDay = datetime.date.today().strftime('%m-%d-%y')
            self.fileNumber = 0
            print("New File Created: {}_{}.json".format(self.currentDay, self.fileNumber))
        else:
            filePath = '{}\\{}_{}.json'.format(data_dir, self.currentDay, self.fileNumber)
            if(os.path.isfile(filePath)):
                if(os.path.getsize(filePath) >= self.MAX_SIZE):
                    self.fileNumber = self.fileNumber + 1
                    print("New File Created: {}_{}.json".format(self.currentDay, self.fileNumber))
            self.outfile = "{}/{}_{}.json".format(data_dir, self.currentDay, self.fileNumber)

    '''
    Flushes the file that is currently being written to every flushTimer minutes.
    
    FlushTimer is declared above current set to 20 minutes
    '''
    def flush_file(self):
        if(time.time() > self.flushEnd):
            with open(self.outfile, 'a') as f:
                f.flush()  # Flushes the internal buffer.
                f.close()
            self.flushStart = time.time()
            self.flushEnd = self.flushStart + self.flushTimer
        return

    '''
    Admin use only. 
    Main purpose of this function is to display updates to the user to notify
    that the program is still doing stuff.
    '''
    def timer_check(self):
        if(time.time() > self.endTime):
            print("{} Tweets, recorded at {}".format(self.tweetCount, datetime.datetime.now()))
            self.startTime = time.time()
            self.endTime = self.startTime + self.timer
            self.tweetCount = 0
        return


if __name__ == '__main__':

    print("Hello world")


    US = [-130.42,27.2,-59.33,49.68,-158.9,15.7,-151.5,22.3,-169.3,54.6,-141.0,71.4]
    UK = [-5.59,49.48,1.76,59.43]
    FR = [-5.08,42.07,7.73,50.03]
    GR = [6.6,48.43,13.97,54.88]
    MX = [-119.28,15.2,-91.23,30.97]
    
    countryCord = {"US": US, "UK": UK, "FR": FR, "GR": GR, "MX": MX}
    
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    try:
        twitter_stream = Stream(auth, MyListener(args.data))
        twitter_stream.filter(track=[args.query], languages=[args.language], locations=countryCord[args.country])
    except:
        print("Error: " + str(sys.exc_info()))
        os.execv(sys.executable, ['python'] + sys.argv)
else:
    print("Yeah")

RestartAt = datetime.datetime.now().replace(hour=23, minute=59,second=59, microsecond=9000)
if datetime.datetime.now() > RestartAt:
    os.execv(sys.executable, ['python'] + sys.argv)