from bs4 import BeautifulSoup
import requests
from write_email_addresses_to_file import writetoFile
import time
from threading import Thread
import re

start = time.time()


def emailExtractor(urlString, emailSet):
    try:
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
                match = re.search(r'[\w\.-]+@[\w\.-]+', str2)
                emailSet.add(match.group(0))
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
        print('Oops! ' + str(e))


homepages = set()
with open('homepages.txt', 'r') as f:
    for homepage in f:
        homepages.add(homepage.replace('\n', ''))

threads = []
emailSet = set()
for homepage in homepages:
    t = Thread(target=emailExtractor, args=(homepage, emailSet))
    threads.append(t)
    t.start()
for x in threads:
    x.join()

writetoFile('email_list.txt', emailSet)
print('From ' + str(len(homepages)) +
      ' homepages got ' + str(len(emailSet)) + ' email')

end = time.time()
print(end - start)
