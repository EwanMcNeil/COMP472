

# 1. A line counter i, followed by 2 spaces.
# 2. The word wi, followed by 2 spaces.
# 3. The frequency of wi in the class story, followed by 2 spaces.
# 4. The smoothed conditional probability of wi in story – P(wi|story), followed by 2 spaces.
# 5. The frequency of wi in the class ask_hn, followed by 2 spaces.
# 6. The smoothed conditional probability of wi in ask_hn – P(wi|ask_hn), followed by 2 spaces.
# 7. The frequency of wi in the class show_hn, followed by 2 spaces.
# 8. The smoothed conditional probability of wi in show_hn – P(wi|show_hn), followed by 2 spaces.
# 9. The frequency of wi in the class poll, followed by 2 spaces.
# 10. The smoothed conditional probability of wi in poll – P(wi|poll), followed by a carriage
# return.


#making 4 dictionarys and getting setting the values there

import csv
import re
import string




storyCount = 0
askCount = 0
showCount = 0
pollCount = 0

def addtoDict(word, postType):
    
    global storyCount
    global askCount
    global showCount 
    global pollCount 

    global wordDictionary
    index = 0
    
    #index of the current type
    if(postType == 'story'):
        storyCount += 1
        index = 0
        
    if(postType == 'ask_hn'):
        askCount += 1
        index = 2
        
    if(postType == 'show_hn'):
        showCount += 1
        index = 4
        
    if(postType == 'poll'):
        pollCount += 1
        index = 6
    
    try:
        valueList = wordDictionary.get(word)
    except KeyError:
        valueList = [0,0,0,0,0,0,0,0]
        #do nothing if its not been created we use default tup
    
    if(valueList == None):
        valueList = [0,0,0,0,0,0,0,0]
    
    wordValue = valueList[index]
    wordValue += 1

    valueList[index] = wordValue


    wordDictionary[word] = valueList
    

wordDictionary = dict()




##reading in the file
with open('hns_2018_2019.csv',encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
           
            postType = row[3]
            title = row[2]
            wordList = re.sub("[^\S]", " ",  title).split()
            for word in wordList:
                word = word.lower()
                addtoDict(word, postType)
            
            line_count += 1
    print(f'Processed {line_count} lines.')
    print("story count", storyCount)
    print("ask count", askCount)
    print("show count", showCount)
    print("pollCount", pollCount)






#creating the percentages 
smoothingFactor = len(wordDictionary)*0.5


# Key: freq story, % story, freq ask_hn, % ask Hn, freq show_hn, % show_hn, freq poll, % poll 
for key in wordDictionary:

    valueList = wordDictionary.get(key)
  
    storyPercent = (valueList[0]+0.5)/(storyCount+smoothingFactor)
    askPercent = (valueList[2]+0.5)/(askCount+smoothingFactor)
    showPercent = (valueList[4]+0.5)/(showCount +smoothingFactor)
    pollPercent = (valueList[6]+0.5)/(pollCount+smoothingFactor)

    valueList[1] = storyPercent
    valueList[3] = askPercent
    valueList[5] = showPercent
    valueList[7]= pollPercent

    wordDictionary[key] = valueList

check = wordDictionary.get("how")
print("check",check)

# for key in wordDictionary:
#     valueList = wordDictionary.get(key)
#     print(key, valueList)
#     print('/n')




#dictary is setup as
# Key: freq story, % story, freq ask_hn, % ask Hn, freq show_hn, % show_hn, freq poll, % poll  







