import requests
from dragnet import content_extractor, content_comments_extractor

# fetch HTML
url = 'https://moz.com/devblog/dragnet-content-extraction-from-diverse-feature-sets/'
r = requests.get(url)

# get main article without comments
content = content_extractor.analyze(r.content)

# get article and comments
content_comments = content_comments_extractor.analyze(r.content)
print content_comments