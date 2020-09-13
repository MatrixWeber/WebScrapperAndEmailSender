from bs4 import BeautifulSoup
import requests
from write_email_addresses_to_file import writetoFile

search_string = 'firma erlangen'
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

# to search
query = search_string

for j in search(query, tld="de", lang='de', num=10, stop=10, pause=2):
    print(j)

#googleSearchUml = "https://www.google.com/search?q=" + search_string + "&start=0"

#r = requests.get(googleSearchUml)
# print(r.content)

urlString = 'https://auto-hartmann-erlangen.seat.de/'

#website = input("Type website here:>\n")
r = requests.get(urlString)  # , auth=('user', 'pass'))


def emailExtractor(urlString):
    emailSet = set()
    r = requests.get(urlString)
    if 200 == r.status_code:
        h = r.content
        soup = BeautifulSoup(h, 'html.parser')
        mailtos = soup.select('a[href^=mailto]')
        for i in mailtos:
            href = i['href']
            try:
                str1, str2 = href.split(':')
            except ValueError:
                break
            emailSet.add(str2)
    return emailSet


emailSet = emailExtractor(urlString)

writetoFile(emailSet)
