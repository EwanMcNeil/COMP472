import csv
import re
import string


string = "The TX-2 Computer and Sketchpad how-to (2012) [pdf],story,jpelecanos,2018-01-03 06:29:04"

res = "".join(filter(lambda x: not x.isdigit(), string)) 

string = str(res)
wordList = re.sub("[, \!?:]+", " ", string).split()

wordOutputList = []
index = 0
for word in wordList:
    res = re.sub(r'\W+', ' ', word)

    if(str(res) != " "):
     word = str(res)
     word = word.lower()
     wordOutputList.append(word)
     index += 1
    
print(wordOutputList)