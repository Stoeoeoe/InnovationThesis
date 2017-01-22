import csv
from csv import DictReader

from nltk.corpus import names
import constants as c




all_classifiers = []
labels = ['electronics', 'wood']
for label in labels:
    all_classifiers += [(label, word.lower()) for word in open(c.DP + '/Data/classifiers/' + label + '.txt').read().split("\n")]

def feature_classifier(text):
    for classifier in all_classifiers:
        if classifier[1] in text:
            return classifier[0]
    else:
        return 'UNKNOWN'

categorized_innovations = []
with open(c.DP + '/Data/clean.csv') as csvFile:
    for row in csv.DictReader(csvFile):
        categorized_innovations.append((row['category'], row['description'] + ' ' + row['summary']))

feature_sets = [(feature_classifier(text.lower().replace("\xa0", "")), text) for (category, text) in categorized_innovations]

for classified in [f for f in feature_sets if f[0] != 'UNKNOWN']:
    print(classified, end = "\r\n")