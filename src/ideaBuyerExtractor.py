import re
import requests
import bs4
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
url = 'http://www.ideabuyer.com';

html = requests.get(url + '/ipavail/index.php', headers=headers).text
soup = bs4.BeautifulSoup(html, 'html.parser')

lists = soup.findAll('ul')
#lists = [tag for tag in lists if tag.get('class') != None and 'listTable' in tag.get('class') ]
ideas = []

for entry in lists[6]:
    link = url + entry.a['href']
    text = requests.get(link).text
    soup = bs4.BeautifulSoup(text, 'html.parser')
    info = soup.find('div', id = 'info')


    idea = {}
    idea['link']        = link
    idea['summary']     = soup.find('div', id ='summary').text.strip()
    idea['author']      = re.match('Posted by (.*) under', info.p.text).group(1)
    idea['category']    = re.match('Posted by .* under (.*)', info.p.text).group(1).replace('"', '')
    idea['type']        = [cell.text.replace(u'\xa0', u' ') for cell in soup.find('div', id = 'info').findAll('td') if cell.img.get('src') == '/img/check.png']
    idea['photo']       = url + soup.find('div', id = 'photo').img.get('src')
    idea['description'] = soup.find('div', id = 'description').text.strip()

    ideas.append(idea)
    try:
        print(idea)
    except:
        print('Invalid character, cannot print in console.')

with open('C://Users//Stoeoeoe//Dropbox//Thesis 2016//Data//innovations.csv', 'w+', newline='') as csvFile:
    fields = sorted([key for key in idea.keys()])
    writer = csv.DictWriter(csvFile, fieldnames= fields)
    writer.writeheader()
    for idea in ideas:
        try:
            writer.writerow(idea)
        except:
            print('Invalid character, cannot print in console.')

