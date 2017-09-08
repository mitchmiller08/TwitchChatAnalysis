import httplib2
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup, SoupStrainer

## Get a list of links on a webpage 'base' that contain 'condition'
def getLinks(base, condition):
    http = httplib2.Http()
    status, response = http.request(base)

    links = []

    for link in BeautifulSoup(response,"html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href') and condition in link['href']:
            links.append(link['href'].replace(' ','%20'))

    return links

## Build a list of streamers with log files availble
def getStreamerList(base):
    streamerlist = getLinks(base,'chatlog')
    streamerlist = [base + i for i in streamerlist]

    return streamerlist

## Build list of link to logs for every active day in 
## months contained in 'monthlist'
def getDailyLinks(base, streamerlink):
    monthlist = ['May','June','July']
    daylist = []

    for month in monthlist:
        temp = getLinks(streamerlink,month)
        if not temp:
            continue   # skip this month if no link exists
        monthlink = temp[0]
        monthlink = base + monthlink
        daylist += getLinks(monthlink,'-')
        daylist = [base + i for i in daylist]
        
    return daylist

def main():
    output = open('streamCount.txt','w')
    # Get all base links
    base = 'https://overrustlelogs.net'
    streamerlist = getStreamerList(base)

    # Build histogram of number of days streamed
    # in May, June, July
    histogram = np.zeros((100,),dtype=np.int)    # 92 possible days
    #count = len(getDailyLinks(base,streamerlist[5]))
    #print(count)
    for streamer in streamerlist:
        print(streamer)
        count = len(getDailyLinks(base,streamer))
        print(count)
        histogram[count] += 1

        output.write(streamer + '\t' + str(count) + '\n')

    output.close()

    # Plot data
    plt.bar(range(100),histogram)
    plt.xlabel('Number of acitve days in May, June, and July')
    plt.ylabel('Number of streamers')
    plt.show()


if __name__ == "__main__":
    main()
