import re
import requests
import bs4
import csv
import string

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
baseUrl = 'https://de.wikipedia.org/wiki/'
wikipediaLetterURL = [baseUrl + 'Gemeinden_der_Schweiz-' + letter for letter in string.ascii_uppercase[:26]]

municipalityWikipediaURLs = []
externalMunicipalityURLs = []
blackListURLs = ['http://www.ag.ch/', 'http://www.ar.ch/', 'http://www.ai.ch/', 'http://www.bl.ch/', 'http://www.bs.ch/', 'http://www.be.ch/', 'http://www.fr.ch/', 'http://www.ge.ch/', 'http://www.gl.ch/', 'http://www.gr.ch/', 'http://www.ju.ch/', 'http://www.lu.ch/', 'http://www.ne.ch/', 'http://www.nw.ch/', 'http://www.ow.ch/', 'http://www.sh.ch/', 'http://www.sz.ch/', 'http://www.sg.ch/', 'http://www.so.ch/', 'http://www.ti.ch/', 'http://www.tg.ch/', 'http://www.ur.ch/', 'http://www.vd.ch/', 'http://www.vs.ch/', 'http://www.zg.ch/', 'http://www.zh.ch/']

for url in wikipediaLetterURL:
    html = requests.get(url, headers=headers).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    newWikipediaSites = ['https://de.wikipedia.org' + link.get('href') for link in soup.select('#mw-content-text > table a') if not link.get('class')]
    if len(newWikipediaSites) == 0:
        newWikipediaSites = ['https://de.wikipedia.org' + link.get('href') for link in
                            soup.select('#mw-content-text > ul a') if not link.get('class')]

    municipalityWikipediaURLs += newWikipediaSites

with open('C://Users//saadk//Dropbox//Thesis 2016//Data//municipalities.csv', 'w+', newline='') as csvFile:
    writer = csv.writer(csvFile)

    for url in municipalityWikipediaURLs:
        html = requests.get(url, headers=headers).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        rows = soup.select('#mw-content-text > table tr')
        externalMunicipalityURLs += [row.td.findNext().a.get('href') for row in rows if
                                     row.td and row.td.get_text() == 'Website:']
        newMunicipality = externalMunicipalityURLs[-1]
        if newMunicipality not in blackListURLs:
            writer.writerow([newMunicipality])
            print(newMunicipality)


