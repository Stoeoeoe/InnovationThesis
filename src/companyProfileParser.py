import bs4;
import requests;
import nltk;
import re;

links = ['http://www.alstom.com', 'http://www.ge.com']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
}
#def getMetaIfHasContent(soup, name, attribute, checkValue, checkAttribute = 'name'):
 #   attr = checkAttribute if checkAttribute is not None else attribute;
 #   [tag.get(attribute) for tag in soup.find_all(name) if tag.get('name') == checkValue and tag.get()]

def getMeta(soup, attribute):
    tags = [meta.get('content') for meta in soup.find_all('meta') if meta.get('name') == attribute and meta.get('content') != None and meta.get('content').strip() != '']
    return tags[0] if len(tags) > 0 else ''

def makeURL(url, link):
    if not url.startswith('/'):
        url = '/' + url
    return link + url.replace('//', '/')

for baseUrl in links:

    # TODO: robots.txt IS A MESS: See alstom.com
    robots = requests.get(baseUrl + '/robots.txt', headers=headers).text
    sitemapXmlURL = [line.split(':')[1].strip() for line in robots.split('\n') if line.split(':')[0] == 'sitemap']
    sitemapXML = requests.get(sitemap)



    html = requests.get(baseUrl, headers=headers).text
    soup = bs4.BeautifulSoup(html, 'html.parser')

    companyProfile = {}

    companyProfile['title'] = soup.title
    companyProfile['description']= getMeta(soup, 'description')
    companyProfile['language']= getMeta(soup, 'language')


    # Parsing-specific
    canonicalLink = soup.find('link', type='canonical').get('href') if soup.find('link', type='canonical') is not None else ''
    navigation = soup.find('nav')

    # Get Bootstrap Carousel to find featured stuff


    # Microformats?

    # Schema-org?

    # RDF?

    # Search for sitemap
    sitemap = [a.get('href') for a in soup.find_all('a') if a.get('href') != None and  'sitemap' in a.get('href')][0]
    sitemap = sitemap if 'http://' in sitemap else baseUrl + sitemap
    print(sitemap)



    # Find about    --> refine
    aboutWords = ['about', 'about-us', 'company']
    sitemapLinks = [a for a in soup.find_all('a') if a.get('href') is not None]
    aboutLinks = []
    for link in sitemapLinks:
        if any(word in link.get('href').lower() for word in aboutWords) or any(word in link.text.lower() for word in aboutWords):
            aboutLinks.append(link.get('href'))
    aboutLinks = list(set(aboutLinks))      # Distinct

    for a in aboutLinks:
        aboutUrl = makeURL(a, baseUrl)
        soup = bs4.BeautifulSoup(requests.get(aboutUrl, headers=headers).text, 'html.parser')
        allDivsWithMain = [div for div in soup.find_all('div')
                           if (div.get('id') is not None and 'main' in div.get('id').lower())
                           or (div.get('class') is not None and True in ['main' in clazz.lower() for clazz in div.get('class')])]



        allMainText = ' '.join([div.text for div in allDivsWithMain]).strip()
        allMainText = re.sub('[ ]+', ' ', allMainText).replace('\r\n', ' ')
        print(allMainText)



    print(companyProfile)
