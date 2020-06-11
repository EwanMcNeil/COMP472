import csv
import re
import string
import nltk
nltk.download('punkt')


title = "The TX-2 Computer and Sketchpad 34 how-to hello's (2012) [pdf],story,jpelecanos,2018-01-03 06:29:04"
word_data = "It originated from the idea that there are readers who prefer learning new skills from the comforts of their drawing rooms"
nltk_tokens = nltk.word_tokenize(title)


words = nltk.word_tokenize(title)


new_words= [word for word in words if word.isalnum()]
i = 0 
for word in new_words:
    new_words[i] = word.lower()
    i += 1

print (nltk_tokens)

print("newWorlds", new_words)
