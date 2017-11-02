import httplib2
import os
import urllib.request as url
from bs4 import BeautifulSoup, SoupStrainer

## Get a list of all users in log for a given streamer
## usernames are stored in a dictionary which is keyed by the 
## month in which they are active
def getUsers(streamer):
    http = httplib2.Http()
    monthlist = ['May','June','July']
    users = {}

    for month in monthlist:
        userlink = 'https://overrustlelogs.net/' + streamer + '%20chatlog/' + month + '%202017/userlogs'
        monthlyusers = []
    
        status,response = http.request(userlink)

        for link in BeautifulSoup(response,"html.parser",parse_only=SoupStrainer('a')):
            if link.has_attr('href') and 'userlogs/' in link['href']:
                user = link['href']
                user = user[user.index('userlogs/')+9:]
                monthlyusers.append(user)
        
        users[month] = monthlyusers

    return users

## Output a list of users from each month to a data
## file for use in other applications
def saveUsers(usersdict,streamer,type):
    outputfile = open(os.path.join(type,streamer) + '.txt','w')
    # Make header with counts
    for month in usersdict:
        outputfile.write(month+'\t'+str(len(usersdict[month]))+'\n')

    outputfile.write('**** BEGIN USERNAME LIST ****\n')

    for month in usersdict:
        outputfile.write(month+'\n')
     
        for user in usersdict[month]:
            outputfile.write("%s\n" % user)

    outputfile.close()
    return

## Get a list of all subscribers in a the selected
## months for a given streamer
def getSubs(streamer):
    monthlist = ['May','June','July']
    subs = {}

    for month in monthlist:
        sublink = 'https://overrustlelogs.net/' + streamer + '%20chatlog/' + month + '%202017/subscribers.txt'
        monthlysubs = []
        
        # Get text on subscriber page
        req = url.Request(sublink, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = url.urlopen(req).read().decode('utf-8')
        webpage = webpage.split('\n')

        # Filter all text that is not usernames by looking for end
        # of notifier ': ' and beginning of subscription type ' j'
        # EXAMPLE: '[2017-05-01 03:51:33 UTC] twitchnotify: USERNAME just subscribed with Twitch Prime!'
        for line in webpage:
            if ': ' and ' j' in line:
                start = line.index(': ') + 2
                end = line.index(' j')
                sub = line[start:end]
                monthlysubs.append(sub)
            # Users that sub while streamer is offline do not have names
            # recorded, only counted
            # EXAMPLE: '[2017-05-19 00:58:28 UTC] twitchnotify: 129 viewers resubscribed while you were away!'
            if 'viewers resubscribed' in line:
                start = line.index(': ') + 2
                end = line.index(' v')
                count = int(line[start:end])
                monthlysubs.extend(['UNKNOWNUSER']*count)

        subs[month] = monthlysubs

    return subs

def main():
    # Get subs and users for each streamer we have data for
    streamers = os.listdir('scores')
    for streamer in streamers:
        print(streamer)
        saveUsers(getUsers(streamer),streamer,'users')
        saveUsers(getSubs(streamer),streamer,'subs')

if __name__ == "__main__":
    main()
