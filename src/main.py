import bs4
import requests
import nltk


sitemapWords = ['sitemap', 'site map', 'uebersicht', 'übersicht', 'inhalt']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

#websites = ['http://www.unterentfelden.ch/', 'http://www.oberentfelden.ch/', 'http://www.suhr.ch/']
websites = ['http://www.suhr.ch/']



def main():
    for website in websites:
        request = requests.get(website, headers=headers)
        text = request.text
        soup = bs4.BeautifulSoup(text, 'html.parser')
        allLinksOnWebsite = filterInvalidUrls([e.get('href') for e in soup.find_all('a')], website)

        sitemapUrl = ''

        for link in allLinksOnWebsite:
            soup = bs4.BeautifulSoup(requests.get(link, headers=headers).text, 'html.parser')
            title = soup.find('title').text.lower()
            if any(word in title for word in sitemapWords):
                sitemapUrl = link
                text = requests.get(sitemapUrl, headers=headers).text
                soup = bs4.BeautifulSoup(text, 'html.parser')
                linksOnSitemap = set(filterInvalidUrls([e.get('href') for e in soup.find_all('a')], website))
                for link in linksOnSitemap:
                    print(link)


def filterInvalidUrls(urls, baseUrl):
    urls = [url for url in urls if url != None]
    urls = [url for url in urls if url and not url.startswith('#') and not url.startswith('mailto')]
    urls = [url if url.startswith('http') else baseUrl + url for url in urls ]
    urls = set(urls)
    return urls

if __name__ == '__main__':
    main()