import httplib2
from bs4 import BeautifulSoup, SoupStrainer

def getLinks(base, condition):
    http = httplib2.Http()
    status, response = http.request(base)

    links = []

    for link in BeautifulSoup(response,"html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href') and condition in link['href']:
            links.append(base + link['href'].replace(' ','%20'))

    return links

## Build a list of streamers with log files availble
def getStreamerList():
    streamerlist = getLinks('https://overrustlelogs.net/','chatlog')

    return streamerlist

## Count the number of days given streamer was active in the months
## contained in 'monthlist'
def countStreams(streamerlink):
    monthlist = ['May','June','July']
    streamcount = 0

    for month in monthlist:
        ###CONTINUE HERE!!!!

def main():
    streamerlist = getStreamerList()
    print(streamerlist[0:10])


if __name__ == "__main__":
    main()
