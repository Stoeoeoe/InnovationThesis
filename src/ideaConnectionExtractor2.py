import re
import requests
import bs4
import csv
import os
import io
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
url = 'https://www.ideaconnection.com';

links = []
#Get first link
link = url + '/new-inventions/?page=1'
html = requests.get(link, headers=headers).text
soup = bs4.BeautifulSoup(html, 'html.parser')
link = [url + '/new-inventions/' + tag.a['href'] for tag in soup.findAll('div', 'list-item')][0]

startLink = ''
#startLink = 'https://www.ideaconnection.com/new-inventions/source-solar-panels-harvest-water-from-the-air-11295.html'
link = link if startLink is '' else startLink

hasNextInvention = True
counter = 1

counter = 1
treshold = 99999

ideas = []
# Go over all links
file = 'C://Users//Stoeoeoe//Dropbox//Thesis 2016//Data//innovations-idea-connection.csv'
fileLaptop = 'C:/Users/saadk/Dropbox/Thesis 2016/Data/innovations-idea-connection.csv'
#folderLocation = 'C:/Users/saadk/Dropbox/Thesis 2016/Data/documents2/'
folderLocation = 'C:/Users/Stoeoeoe/Dropbox/Thesis 2016/Data/documents2/'

while counter < treshold and hasNextInvention:
    text = requests.get(link).text
    soup = bs4.BeautifulSoup(text, 'html.parser')

    title = soup.find('h1').text
    imgages = ['http:' + img.get('src') for img in soup.find_all('img', alt=title)] if soup.find('img', alt=title) else ''
    date = soup.find('div', 'col8').i.text if (soup.find('div', 'col8') != None and soup.find('div', 'col8').i != None) else ''
    description = re.match('([\W\w\r\n]*)(?:More Info).*', soup.find('div', 'col8').text.replace(title, '').replace(date, '')).group(1).strip()
    video = [iframe for iframe in soup.find_all('iframe')][0].get('src').replace('/embed/', '/watch?v=') if soup.find('iframe') else ''
    links = [link.get('href') for link in soup.find_all('a', 'standard10')]

    try:
        link = [url + '/new-inventions/' + link.get('href') for link in soup.find_all('a') if 'Next Invention' in link.text][0]
    except:
        hasNextInvention = False

    idea = {'title': title, 'img': imgages, 'date': date, 'description': description, 'video': video, 'links': links, 'link': link}
    ideas.append(idea)


    #Corpus
    try:
        with open(folderLocation + str(counter), 'w+', newline='') as file:
            file.write(idea['description'])

        #Json
        with open(folderLocation + 'json/' + str(counter) + '.json', 'w+', newline='') as file:
            file.write(json.dumps(idea, sort_keys=True, indent=4))
    except Exception as ex:
        print(ex)

    #1574 causes problems

    print(str(counter) + ':' + title)
    title = None; img = None; date = None; description = None; video = None; links = None;
    counter += 1