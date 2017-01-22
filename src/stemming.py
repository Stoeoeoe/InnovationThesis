from nltk import stem
from nltk import tokenize
from nltk import tag
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

text1 = 'His acting was amazing.'
text2 = 'He was merely acting.'


print(pos_tag(word_tokenize(text1)))
print(pos_tag(word_tokenize(text2)))