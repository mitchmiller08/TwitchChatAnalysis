import nltk

## Load the log text into a list of individual messages
def loadLog(filepath):
    logfile = open(filepath)
    messagelist = []
    for line in file.readlines():
        messagelist.append(line.strip())

    return messagelist

## Split timestamp, username, and message text from
## a raw logfile line
def separateMessage(rawmessage):
    timestampend = rawmessage.index(']') + 1
    timestamp = rawmessage(:timestampend)

    userend = rawmessage[timestampend:].index(':') + timestampend + 1
    user = rawmessage[timestampend+1:userend-1]

    message = rawmessage[userend+1:]

    return timestamp, user, message



## NOTES:   from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
##          sia = SIA()
##          score = sia.polarity_scores(SOMETEXT)
##          score gives neg, neu, pos, and compound score

## TODO:    Figure out how to average scores
##          Get user / subscriber count
##          Calculate message frequency from timestamps
##          Do analysis
