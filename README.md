## Command line tool to collect tweets data by keywords and date range

1. Make sure you have python installed and import tweepy package.

Follow this link to learn about TweePy package

https://github.com/tweepy/tweepy

2. Rename file config.py.dist to config.py

3. Edit config.py with your app authentication tokens

4. Enjoy the command line

## Usage
```
python run.py --startDate=YYYY-MM-DD --endDate=YYYY-MM-DD --keyword=your-key-word
```

## Sample Result
We download tweets related to Harvey storm available at this link:

https://drive.google.com/drive/folders/0Bz0t5Fi0GA75bzNpWVhaSElOOVU

## Command line tool to calculate term frequency from the twitter data 

* **term-frequency.py** calculator looks for *.json* files that are output by **run.py**
* This program only outputs command line information, so take note of the console output

### Commands

**Directory:** `-d | --dir` will allow the program to know where the *.json* files are located. Folder/Files must be in the tweet-collector root

**Stopwords:** `-sw | --stopwords` will block any additional words that you want to remove from the frequency calculator

**Frequency Count:** `-fc | --freqCount` will set the N number up terms that will be displayed 

```
python term-frequency.py --dir=output/ --stopwords=opioid,rt,day,calm --freqCount=3

addiction       1045
epidemic        987
overdose        665
```


## Classifiers to learn from this dataset

https://github.com/litpuvn/harvey-classifier


## Twitter Error Return Code

https://developer.twitter.com/en/docs/basics/response-codes

## Twitter Tweet Object

**JSON Example:** https://gist.github.com/hrp/900964

**Tweet Object Documentation:** https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object

*Note: There are various kinds of coordinates. 'place', 'coordinates', 'geo'. Place has the capability of telling us where the tweet came from, giving us 4 sets of coordinates that represent a box however it does not neccessarly mean the tweet came from there. Goe is not longer be supported by Twitter. Coordinates, if not null, is the point location of where the tweet came from. Use coordinates, else use place.*

## Authors

Long: https://github.com/litpuvn

Joshua: https://github.com/JStuve

Yusuf: https://github.com/yusufmurat

## Reference

The code is learnt from this blog

https://dev.to/bhaskar_vk/how-to-use-twitters-search-rest-api-most-effectively
