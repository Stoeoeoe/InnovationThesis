import re
import requests
import bs4
import csv
import string

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.PhantomJS(executable_path='../bin/phantomjs-2.1.1-windows/bin/phantomjs.exe', service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver.set_window_size(1920, 1080)
wait = WebDriverWait(driver, 20)

def waitForIFrame():
    if 'iframe' in driver.page_source:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "iframe")))
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe"));


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
baseUrl = 'https://de.wikipedia.org/wiki/'
sitemapKeywords = ['Sitemap', 'sitemap', 'Inhaltsverzeichnis', 'Übersicht', 'Plan du site']
companiesKeywords = ['Gewerbe', 'Firmenverzeichnis', 'Firmen', 'Unternehmen']

# FOR PAPER: Use Sitemap or traverse all links (like 3)

with open('C://Users//saadk//Dropbox//Thesis 2016//Data//municipalities-en.csv', 'r+', newline='') as csvFile:
    reader  = csv.reader(csvFile)
    for url in reader:
        sitemap = ''
        site = ''

        baseUrl = url[0] if not url[0].endswith('/') else url[0][0:-1]
        print('Now checking ' + baseUrl)

        driver.get(baseUrl)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body")))
        waitForIFrame()
        html = driver.page_source
        #html = requests.get(baseUrl, headers=headers).text
        soup = bs4.BeautifulSoup(html, 'html.parser')


        allLinks = soup.find_all('a')
        sitemapCandidates = [link.get('href') for link in allLinks if link.text and link.get('href') and not link.get('href').startswith('_') and (any([keyword in link.text for keyword in sitemapKeywords]) or any([keyword in link.get('href') for keyword in sitemapKeywords]))]
        if len(sitemapCandidates) > 0:
            sitemap = sitemapCandidates[0]
            if baseUrl not in sitemap:
                sitemap = baseUrl + sitemap
            print('Found sitemap: ' + sitemap)
            driver.save_screenshot('C:/tmp/chueche/rab.png')
            driver.quit()


        else:
            print('No sitemap.')
            continue

        driver.get(sitemap)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body")))
        waitForIFrame()
        html = driver.page_source
#        html = requests.get(sitemap, headers=headers).text

        soup = bs4.BeautifulSoup(html, 'html.parser')
        allLinks = set(tag for tag in soup.find_all('a'))
        companiesSites = [link for link in allLinks if link.text and link.text in companiesKeywords]
        if len(companiesSites ) > 0:
            site = companiesSites[0].get('href')
            if baseUrl not in site:
                site = baseUrl + site

            print('Found a commerce website: ' + site)
            driver.get(site)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body")))
            html = driver.page_source
            waitForIFrame()
                #            html = requests.get(site, headers=headers).text
            soup = bs4.BeautifulSoup(html, 'html.parser')
            allCompanies = [link for link in soup.find_all('a') if link.get('href') and not link.get('href').startswith('#') and not link.get('href').startswith('/') and not link.get('href').startswith(baseUrl) and not link.get('href').startswith('mailto') and (link.get('href').startswith('http://') or link.get('href').startswith('www.'))]
            print(allCompanies)

