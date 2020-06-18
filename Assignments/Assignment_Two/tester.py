import csv
import re
import string
import nltk
nltk.download('punkt')





def tokenAndFilter(title):
    nltk_tokens = nltk.word_tokenize(title)
    tokenizedWords = nltk.word_tokenize(title)


    i = 0
    for word in tokenizedWords:
        tokenizedWords[i] = word.lower()
        i += 1

    #lower the tokens and compare what we've filtered out

    new_words = []

    #filters out digits
    #new_words= [word for word in words if word.isalnum()]
    #new_words = [x for x in words if not any(c.isdigit() for c in x)]
    a = "1234567890"
    i = 0
    for word in tokenizedWords:
        for char in a:
            word = word.replace(char,"")
        new_words.append(word)
        i+= 1

    a = "_)([{]},':;-"
    i = 0
    for word in new_words:
        for char in a:
            word = word.replace(char,"")
        new_words[i] = word
        i+= 1
        

    i = 0
    for word in new_words:
        new_words[i] = word.lower()
        if word == '':
            del new_words[i]
        i += 1

    removedWords =  []
    for word in tokenizedWords:
        if not word in new_words:
            if not word in removedWords:
                removedWords.append(word)

    print (nltk_tokens)

    print("newWorlds", new_words)

    print("removedWords", removedWords)




title = "The TX-2 Computer and Sketchpad 34 how-to hello's (2012) [pdf],story,jpelecanos,2018-01-03 06:29:04"
word_data = "It originated from the idea that there are readers who prefer learning new32 skills from the comforts of their drawing rooms"

tokenAndFilter(title)

tokenAndFilter((word_data))