import os
import nltk
from nltk.stem import SnowballStemmer


where = 'C:/Users/saadk/Dropbox/Thesis 2016/Data/Patent Text Categorized'
whereOut = 'C:/Users/saadk/Dropbox/Thesis 2016/Data/Patent Text Categorized Cleaned'

folders = os.listdir(where)
files = []
stemmer = nltk.LancasterStemmer('english')
tokenizer = nltk.tokenize.WhitespaceTokenizer()
wnl = nltk.WordNetLemmatizer()

count = 0
end = sum([len(os.listdir(where + '/' + dir)) for dir in os.listdir(where)])
for folder in folders:
    #console.log(str(count) + '/' + str(end))
    files = os.listdir(where + '/' + folder)

    for file in files:
        with open(where + '/' + folder + '/' + file, 'r', encoding='UTF-8') as f:
            text = f.read()
            tokenized = tokenizer.tokenize(text)
            words = []
            for word in tokenized:
                words.append(wnl.lemmatize(word))
#                words.append(stemmer.stem(word))

            if not os.path.isdir(whereOut + '/' + folder):
                os.mkdir(whereOut + '/' + folder)
            with open(whereOut + '/' + folder + '/' + file, 'w+', encoding='UTF-8') as fileOut:
                fileOut.write(' '.join(words))

    count += 1