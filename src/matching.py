import nltk
from nltk.corpus import brown

from nltk.corpus import PlaintextCorpusReader
corpus_root = 'C://Users//Stoeoeoe//Dropbox//Thesis 2016//Data//documents'
corpus = PlaintextCorpusReader(corpus_root, '.*\.txt', encoding='utf-8')

cfd = nltk.ConditionalFreqDist(
          (genre, word)
          for genre in brown.categories()
          for word in brown.words(categories=genre))

print(wordlists.words("1.txt"))
