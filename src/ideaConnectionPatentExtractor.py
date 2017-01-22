import bs4
import requests
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
patentsPage = 'https://www.ideaconnection.com/patents/'

html =  requests.get(patentsPage, headers=headers).text
soup = bs4.BeautifulSoup(html, 'html.parser')

categoryLinks = [tag.a.get('href') for tag in soup.find_all('h3', 'grey')]

#folderLocation = 'C:/Users/saadk/Dropbox/Thesis 2016/Data/patents/'
folderLocation = 'C:/Users/Stoeoeoe/Dropbox/Thesis 2016/Data/patents/'


counter = 1

for category in categoryLinks:
    html = requests.get('https://www.ideaconnection.com/patents/' + category, headers=headers).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    categoryName = soup.find('h1', 'head').text.replace('for Sale or License', '')
    patentLinks = [tag.a.get('href') for tag in soup.find_all('h3', 'grn_heading vcut')]
    for patentLink in patentLinks:
        html = requests.get('https://www.ideaconnection.com/patents/' + patentLink, headers=headers).text
        soup = bs4.BeautifulSoup(html, 'html.parser')

        contentTag = soup.find('div', 'content-wrapper full-article').find('div', 'col8')
        title = contentTag.h1.text
        try:
            fullDescription = re.match('([\W\w\r\n]*)(?:Attached files:).*', contentTag.text.replace(title, '')).group(1).strip()
        except:
            try:
                fullDescription = re.match('([\W\w\r\n]*)(?:Patents:).*', contentTag.text.replace(title, '')).group(1).strip()
            except:
                fullDescription = re.match('([\W\w\r\n]*)(?:Type of Offer:).*', contentTag.text.replace(title, '')).group(1).strip()

        images = [img.get('src') for img in contentTag.find_all('img')]

        videos = [iframe.get('src').replace('/embed/','/watch?v=') for iframe in soup.find_all('iframe')]

        #patentTag = [b for b in contentTag.find_all('b') if b.text == 'Patents:'][0]
        type = contentTag.find(text= 'Type of Offer:').next_element.strip()
        inventors = contentTag.find(text= 'Inventor(s):').next_element.strip() if contentTag.find(text = 'Inventor(s):') else ''
        askingPrice = contentTag.find(text= 'Asking Price:').next_element.strip() if contentTag.find(text = 'Asking Price:') else ''
#        hasNextPatent = True if patentTag != None else False
        idea = {"title": title, "description": fullDescription, "link": patentLink, "category": categoryName, 'type': type, 'askingPrice': askingPrice, 'images': images, 'videos': videos, 'inventors': inventors }

#        while(hasNextPatent):
 #           patentTag


        # Corpus
        try:
            with open(folderLocation + str(counter), 'w+', newline='') as file:
                file.write(idea['description'])

            # Json
            with open(folderLocation + 'json/' + str(counter) + '.json', 'w+', newline='') as file:
                file.write(json.dumps(idea, sort_keys=True, indent=4))
        except Exception as ex:
            print(ex)
        except:
            pass
        counter += 1
        print(idea)