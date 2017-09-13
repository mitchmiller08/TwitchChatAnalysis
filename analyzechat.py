import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import os import listdir
from os.path import join

## Build a list of logfiles saved locally
def getLogList():
    loglist = {}

    for streamer in os.listdir('logs'):
        streamerpath = join('logs',streamer)
        loglist[streamer] = [join(streamerpath,log) for log in os.listdir(streamerpath)]

    return loglist

## Load the log text into a list of individual messages
def loadLog(filepath):
    logfile = open(filepath)
    messagelist = []
    for line in logfile.readlines():
        messagelist.append(line.strip())

    return messagelist

## Split timestamp, username, and message text from
## a raw logfile line
def separateMessage(rawmessage):
    timestampend = rawmessage.index(']') + 1
    timestamp = rawmessage[:timestampend]

    userend = rawmessage[timestampend:].index(':') + timestampend + 1
    user = rawmessage[timestampend+1:userend-1]

    message = rawmessage[userend+1:]

    return timestamp, user, message

##  Calculates the sentiment scores of 'message
##  Returns a dictionary with keys 'pos', 'neu',
##  'neg', and 'compunt'
def analyzeMessage(message):
    sia = SIA()
    scores = sia.polarity_scores(message)

    return scores

def main():
    logList = getLogList()
    for streamer in list(logList.keys()):
        ## DO SOMETHING WITH logList[streamer] (list of log file paths)

if __name__ == '__main__':
    main()

## NOTES:   from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
##          sia = SIA()
##          score = sia.polarity_scores(SOMETEXT)
##          score gives neg, neu, pos, and compound score
##          avgpos = sum(score['pos'] for score in scoreslist) / len(scoreslist

## TODO:    Figure out how to average scores
##          Get user / subscriber count
##          Calculate message frequency from timestamps
##          Do analysis
