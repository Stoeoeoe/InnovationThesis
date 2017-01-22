import csv

with open('C://Users//Stoeoeoe//Dropbox//Thesis 2016//Data//clean.csv') as csvFile:
    reader = csv.DictReader(csvFile)
    i = 0
    for row in reader:
        i+=1
        with open('C://Users//Stoeoeoe//Dropbox//Thesis 2016//Data//documents/' + str(i) + '.txt', 'w', encoding='utf-8') as file:
            file.write(row['description'],)