from datetime import datetime
from os.path import join
from os import listdir
import matplotlib.pyplot as plt

## Get sentiment scores calculated from analyzechat.py
## Split them by month
## Returns a dictionary, keyed by month, of strings
## in the form "AVG STD" for each type of sentiment
def getScores(streamer):
    scorefile = open('scores/'+streamer)
    lines = scorefile.readlines()
    months = ['May','June','July']
    pos,neu,neg,cmp = {}, {}, {}, {}

    for month in months:
        pos[month] = []
        neu[month] = []
        neg[month] = []
        cmp[month] = []

    for line in lines:
        scores = line.split('\t')
        datestring= scores[0].strip('.log')
        date = datetime.strptime(datestring,'%Y-%m-%d')
        month = date.strftime('%B')

        pos[month].append(scores[1])
        neu[month].append(scores[3])
        neg[month].append(scores[5])
        cmp[month].append(scores[7])

    scorefile.close()
    return pos,neu,neg,cmp

## Calculate the average and new standard deviation
## of a dictionary of scores
## Returns a list of averages and standard deviations for each month available
def averageScores(scores):
    average = []
    stdev = []
    
    for month in scores:
        n = len(scores[month])
        if n != 0:
            values = [float(i.split(' ')[0]) for i in scores[month]]
            stdevs = [float(i.split(' ')[1]) for i in scores[month]]

            average.append(sum(values)/n)
            stdev.append((sum(i*i for i in stdevs) / n**2) ** 0.5)
        else:
            average.append(0)
            stdev.append(0)

    return average, stdev

## Get user counts calculated from countusers.py
## Takes a type ('users' or 'subs') as input and returns
## a list of monthly usercount
def getUsers(type,streamer):
    users = []
    userfile = open(join(type,streamer)+'.txt')
    lines = userfile.readlines()
    endpoint = lines.index('**** BEGIN USERNAME LIST ****\n')
    
    for i in range(endpoint):
        month, count = lines[i].split()
        users.append(int(count))

    return users

## Collect user and sub counts and average scores into
## lists for plotting
## Returns two lists of user ans sub counts
## and two dictionaries keyed by the score type of
## average scores and standard deviation
def organizeData():
    streamers = listdir('scores')
    streamers.sort()
    totalusers = []
    totalsubs = []
    scoresav = {}
    scoressd = {}
    types = ['pos','neu','neg','cmp']

    for scoretype in types:
        scoresav[scoretype] = []
        scoressd[scoretype] = []

    for streamer in streamers:
        pos,neu,neg,cmp = getScores(streamer)
        users = getUsers('users',streamer)
        subs = getUsers('subs',streamer)
        tempdict = {}

        tempdict['pos'] = averageScores(pos)
        tempdict['neu'] = averageScores(neu)
        tempdict['neg'] = averageScores(neg)
        tempdict['cmp'] = averageScores(cmp)

        totalusers += users
        totalsubs += subs

        for scoretype in types:
            scoresav[scoretype] += tempdict[scoretype][0]
            scoressd[scoretype] += tempdict[scoretype][1]

    return totalusers, totalsubs, scoresav, scoressd

def main():
    totalusers, totalsubs, scoresav, scoressd = organizeData()

    plt.plot(totalusers, scoresav['cmp'], 'ro')
    plt.plot(totalsubs,scoresav['cmp'],'bo')
    #plt.plot(scoresav['cmp'],totalusers,'ro')
    plt.show()

if __name__ == "__main__":
    main()
