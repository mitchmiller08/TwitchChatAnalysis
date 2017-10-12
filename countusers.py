import httplib2
import os
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

def saveUsers(usersdict,streamer):
    outputfile = open('users/' + streamer + '.txt','w')
    months = list(userdict.keys())
    for month in months:
        ## CONTINUE HERE
        ## OUTPUT MONTH FOLLOWED BY LIST OF USERS

def getSubs(streamer):
    monthlist = ['May','June','July']
    sublinks = []

    for month in monthlist:
        sublinks.append('https://overrustlelogs.net/' + streamer + '%20chatlog/' + month + '%202017/subscribers')



def main():
    test = getUsers('Day9tv')
    print(len(test['May']))
    print(len(test['June']))
    print(len(test['July']))

if __name__ == "__main__":
    main()
