import urllib.request as url
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import os

## Get a list of links on a webpage 'base' that contain 'condition'
def getLinks(base, condition):
    http = httplib2.Http()
    status, response = http.request(base)

    links = []

    for link in BeautifulSoup(response,"html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href') and condition in link['href']:
                links.append(link['href'].replace(' ','%20'))

    return links

## Build list of active days for given streamer
def getDailyLink(base, streamer):
    monthlist = ['May','June','July']
    daylist = []

    for month in monthlist:
        temp = getLinks(streamer,month)
        if not temp:
            continue
        monthlink = temp[0]
        monthlink = base + monthlink
        daylist += getLinks(monthlink,'2017-')
        
    daylist = [base + i for i in daylist]

    return daylist

## Get contents of logfile at link
def getLogText(link):
    req = url.Request(link, headers={'User-Agent': 'Mozilla/5.0'})  # Pretend to be a Firefox browser
    webpage = url.urlopen(req).read()
    return webpage

## Make directory for log files to go in and return path
def mkdir(streamer):
    name = streamer[27:-10]     # Strip url base and chatlog suffix
    path = 'logs/' + name
    print(name)
    if not os.path.exists(path):
        os.makedirs(path)       # Make directory for streamer's logs if none exists

    return path

## Get and save logfiles
def saveLogs(path, daylist):
    for day in daylist:
        log = getLogText(day + '.txt')
        date = day[-10:]

        outputfile = open(path +'/'+date+'.log','wb')
        outputfile.write(log)
        outputfile.close()

def main():
    base = 'https://overrustlelogs.net'
    ## Build a list of streamers that were active everyday
    ## in May, June, and July (deal with duplicate logs later)
    streamerfile = open('streamCount.txt','r')
    threshold = 91
    streamerlist = []
    for line in streamerfile:
        streamer, count = line.split()
        if int(count) > threshold:
            streamerlist.append(streamer)

    ## Make appropriate directories and save logs
    for streamer in streamerlist:
        path = mkdir(streamer)

        daylist = getDailyLink(base, streamer)
        ## Get log for each day and save to streamer's directory
        saveLogs(path, daylist)

if __name__ == "__main__":
    main()
