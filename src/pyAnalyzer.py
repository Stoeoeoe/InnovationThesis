import os

dir = "C:/Users/saadk/Dropbox/Thesis 2016/Data/documents2/json/"
files = os.listdir(dir)
for file in files:
    os.rename(dir + file, dir +  file + '.json')