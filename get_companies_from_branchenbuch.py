from threading import Thread

from selenium import webdriver
from time import sleep


def get_homepages(homepage):
    browser = webdriver.Chrome('C:/Users/SW/workspace/chromedriver')
    browser.get(homepage)
    #sleep(2)
    elems = browser.find_elements_by_css_selector("#resultatDivId [href]")
    links_and_spam = [elem.get_attribute('href') for elem in elems]
    links = set()
    homepages = set()
    with open('homepages.txt', 'a') as f:
        for linkAndSpam in links_and_spam:
            if 'https' in linkAndSpam:
                links.add(linkAndSpam)
        try:
            for link in links:
                browser.get(link)
                sleep(1)
                results = browser.find_elements_by_css_selector(
                    R'#productDetailUpdateable > div.container.containerCompany > div.row.row10 > '
                    R'div.col-xs-12.col-sm-6.col-md-8.companyCol > div:nth-child(1) > div:nth-child(1) > '
                    R'div > div.companyWeb > div.listWww [href]')
                if len(results):
                    for result in results:
                        f.write(result.text + '\n')
        except:
            pass


#threads = []
for i in range(0, 10):
    url = "https://de.kompass.com/d/erlangen/de_09_09562/page-" + str(i) + "/"
    print(url)
    get_homepages(url)
    #t = Thread(target=get_homepages, args=url)
    #threads.append(t)
    #t.start()
#for x in threads:
 #   x.join()
