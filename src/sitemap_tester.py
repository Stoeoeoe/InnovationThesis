import requests
import csv
import re
from multiprocessing import Pool
import portalocker
from multiprocessing import Process


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}


def handle_links(linkList):
    for link in links:
        try:
            response = requests.get(link + fileType, headers = headers, timeout=2000)
            sites[link] = response.status_code

            if response.status_code is 200:
                name = re.match('https?:\/\/(?:www\.)?(.*)(?:\.\w\w\w?)', link).group(1)
                with open(fileOutFolder + name, 'w+', encoding='utf-8') as file:
                    file.write(response.text)
            print(link + ': ' + str(response.status_code))
        except:
            sites[link] = 404

    print(sites)
    with open(filePathResults, 'a+') as file:
        portalocker.lock(file)
        writer = csv.writer(file)
        portalocker.unlock(file)
        for key in sites.keys():
            writer.writerow([key, sites[key]])

filePath = '../Data/Fortune 500/fortune500_links.txt'
sites = {}

#sitemap
fileOutFolder = '../Data/Fortune 500/fortune500_hasSitemap.txt'
fileOutFolder  = '../Data/Fortune 500/sitemaps/'
fileType = '/sitemap.xml'

#sitemap
fileOutFolder = '../Data/Fortune 500/fortune500_hasSitemap-non-xml.txt'
fileOutFolder  = '../Data/Fortune 500/sitemaps-non-xml/'
fileType = '/sitemap'



fileOutFolder = '../Data/Fortune 500/robots/'
filePathResults = '../Data/Fortune 500/fortune500_hasRobots.txt'
fileType = '/robots.txt'


if __name__ == '__main__':
    with open(filePath, 'r', newline='') as file:
        links = file.read().split('\r\n')
        # 4 Batches
        for i in range(1, 4):
            p = Process(target=handle_links, args=links[i * 0:i * 125])
            p.start()
            p.join()

