from selenium import webdriver
from time import sleep

browser = webdriver.Chrome(
    '/Users/alexanderweber/Documents/GitHub/python_projects/WebScrapperAndEmailSender/chromedriver')

browser.get("https://de.kompass.com/d/erlangen/de_09_09562/page-2/")

sleep(1)
elems = browser.find_elements_by_css_selector("#resultatDivId [href]")
linksAndSpam = [elem.get_attribute('href') for elem in elems]
links = set()
homepages = set()
with open('homepages.txt', 'a') as f:
    for linkAndSpam in linksAndSpam:
        if 'https' in linkAndSpam:
            links.add(linkAndSpam)
    for link in links:
        browser.get(link)
        sleep(1)
        results = browser.find_elements_by_css_selector(
            '#productDetailUpdateable > div.container.containerCompany > div.row.row10 > div.col-xs-12.col-sm-6.col-md-8.companyCol > div:nth-child(1) > div:nth-child(1) > div > div.companyWeb > div.listWww [href]')
        for result in results:
            f.write(result.text + '\n')
