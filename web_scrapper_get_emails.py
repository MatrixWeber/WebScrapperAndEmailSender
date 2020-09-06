from bs4 import BeautifulSoup
import requests
from write_email_addresses_to_file import writetoFile

urlString = 'https://auto-hartmann-erlangen.seat.de/'

#website = input("Type website here:>\n")
r = requests.get(urlString) #, auth=('user', 'pass'))

def emailExtractor(urlString):
    emailSet = set()
    r = requests.get(urlString)
    if 200 == r.status_code:
        h = r.content
        soup=BeautifulSoup(h,'html.parser')
        mailtos = soup.select('a[href^=mailto]')
        for i in mailtos:
            href=i['href']
            try:
                str1, str2 = href.split(':')
            except ValueError:
                break
            emailSet.add(str2)
    return emailSet

emailSet = emailExtractor(urlString)

writetoFile(emailSet)