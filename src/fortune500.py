import bs4
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

url = 'http://beta.fortune.com/global500/'
html = requests.get(url, headers).text

soup = bs4.BeautifulSoup(html, 'html.parser')
print(soup.text)