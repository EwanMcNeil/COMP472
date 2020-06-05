

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
    if(postType is 'story'):
        storyCount += 1
        index = 0
        
    if(postType is 'ask_hn'):
        askCount += 1
        index = 2
        
    if(postType is 'show_hn'):
        showCount += 1
        index = 4
        
    if(postType is 'poll'):
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

            res = "".join(filter(lambda x: not x.isdigit(), title)) 
            string = str(res)
            wordList = re.sub("[, \!?:]+", " ", string).split()

            wordOutputList = []
            for word in wordList:
                res = re.sub(r'\W+', ' ', word)

                if(str(res) != " "):
                    word = str(res)
                    word = word.lower()
                    wor = word.strip()
                    wordOutputList.append(word)

            for word in wordOutputList:
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
  
    storyPercent = ((valueList[0]+0.5)/(storyCount+smoothingFactor))
    askPercent = ((valueList[2]+0.5)/(askCount+smoothingFactor))
    showPercent = ((valueList[4]+0.5)/(showCount +smoothingFactor))
    pollPercent = ((valueList[6]+0.5)/(pollCount+smoothingFactor))

    valueList[1] = storyPercent
    valueList[3] = askPercent
    valueList[5] = showPercent
    valueList[7]= pollPercent

    wordDictionary[key] = valueList

check = wordDictionary.get("how")
print("check",check)


#sorting a list for the output file
sortedkeys = []
for key in wordDictionary:
    sortedkeys.append(key)

sortedkeys.sort()

f = open("model-2018.txt", "w")
i = 0
for key in sortedkeys:
    
    stringtoWrite = str(i) + " " + key + " "
    outputFromDict = wordDictionary.get(key)
    for value in outputFromDict:
        stringtoWrite = stringtoWrite + " " + str(value)
    print(stringtoWrite)
    try:
        f.write(stringtoWrite)
    except UnicodeEncodeError:
        print("errror skipping")
        # stringtoWrite = stringtoWrite.encode().decode("utf-8")
        # f.write(stringtoWrite)
    f.write('\n')
    i += 1
f.close()

    





#dictary is setup as
# Key: freq story, % story, freq ask_hn, % ask Hn, freq show_hn, % show_hn, freq poll, % poll  







