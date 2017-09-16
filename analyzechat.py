import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from os import listdir
from os.path import join, basename
import numpy as np
from multiprocessing import Pool
from functools import partial

## Check if this streamer has already been
## analyzed in a previous run of program
def checkProgress(streamer):
    if streamer in listdir('scores'):
        scorefile = join('scores',streamer)
        with open(scorefile,'r') as f:
            lastline = f.readlines()[-1]

        lastcompletedlog = lastline.split()[0]
        if lastcompletedlog == '2017-07-31.log':
            lastcompletedlog = 'done'
        return lastcompletedlog
    else:
        return ''

## Build a list of logfiles saved locally
def getLogList():
    loglist = {}

    for streamer in listdir('logs'):
        streamerpath = join('logs',streamer)
        loglist[streamer] = [join(streamerpath,log) for log in listdir(streamerpath)]
        loglist[streamer].sort()

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

## Split all messages in a given logfile
def separateMessages(rawmessagelist):
    timestamplist, usernamelist, messagelist = [],[],[]
    for rawmessage in rawmessagelist:
        timestamp, username, message = separateMessage(rawmessage)
        timestamplist.append(timestamp)
        usernamelist.append(username)
        messagelist.append(message)

    return timestamplist, usernamelist, messagelist

## Calculates the sentiment scores of 'message
## Returns a dictionary with keys 'pos', 'neu',
## 'neg', and 'compunt'
def analyzeMessage(message):
    sia = SIA()
    scores = sia.polarity_scores(message)

    return scores

## Do sentiment analysis on all messages in a list 
## Return the average and standard deviation of scores
## for negative, positive, neutral, and compound
def analyzeMessages(messagelist):
    poslist,neglist,neulist,compoundlist = [],[],[],[]
    for message in messagelist:
        scores = analyzeMessage(message)
        poslist.append(scores['pos'])
        neglist.append(scores['neg'])
        neulist.append(scores['neu'])
        compoundlist.append(scores['compound'])

    negativeresults = [np.mean(neglist),np.std(neglist)]
    positiveresults = [np.mean(poslist),np.std(poslist)]
    neutralresults = [np.mean(neulist),np.std(neulist)]
    compoundresults = [np.mean(compoundlist),np.std(compoundlist)]

    return negativeresults, neutralresults, positiveresults, compoundresults

## Format scores for output to file
def formatOutput(logpath,negres,neures,posres,compres):
    output = basename(logpath)
    output += '\t' + str(negres[0]) + ' ' + str(negres[1]) + '\t'
    output += '\t' + str(neures[0]) + ' ' + str(neures[1]) + '\t'
    output += '\t' + str(posres[0]) + ' ' + str(posres[1]) + '\t'
    output += '\t' + str(compres[0]) + ' ' + str(compres[1]) + '\n'
    return output

def analyzeStreamer(streamer,loglist):
    print('Beginning '+streamer)
    lastcompletedlog = checkProgress(streamer)

    if lastcompletedlog == 'done':
        return

    elif lastcompletedlog == '':
        scoresfile = open(join('scores',streamer),'w')
        index = 0
    
    else:
        scoresfile = open(join('scores',streamer),'a')
        index = loglist[streamer].index(join('logs',streamer,lastcompletedlog)) + 1

    logpaths = loglist[streamer]
    for logpath in logpaths[index:]:
        print(basename(logpath))
        rawmessagelist = loadLog(logpath)
        timestamplist, usernamelist, messagelist = separateMessages(rawmessagelist)

        negativeresults, neutralresults, positiveresults, compoundresults = analyzeMessages(messagelist)
        scoresfile.write(formatOutput(logpath,negativeresults,neutralresults,positiveresults,compoundresults))

    scoresfile.close()
    return

def main():
    p = Pool(4)
    logList = getLogList()
    
    # Evaluate analyzeStreamer using Pool of 4 processors.
    p.map(partial(analyzeStreamer, loglist=logList),list(logList.keys()))

#    for streamer in loglist.keys()
#        analyzeStreamer(streamer,loglist)

if __name__ == '__main__':
    main()

## NOTES:   from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
##          sia = SIA()
##          score = sia.polarity_scores(SOMETEXT)
##          score gives neg, neu, pos, and compound score
##          avgpos = sum(score['pos'] for score in scoreslist) / len(scoreslist

## TODO:    Sort log files before analysis 
##          Get user / subscriber count
##          Calculate message frequency from timestamps
