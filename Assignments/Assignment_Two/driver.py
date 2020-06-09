

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
import math





##functions
def addtoDict(word, postType, Experiment):
    
    global storyCount
    global askCount
    global showCount 
    global pollCount 
    global stopWordList
    global stopWordDictionary
    global baselineDictionary
    index = 0

    if(Experiment == 1):
        ##indicating its the stop one
        if (word in stopWordList):
           return
    
    #index of the current type
    if(postType == 'story'):
        print("story")
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
        if(Experiment == 1):
            valueList = stopWordDictionary.get(word)
        ##indicating its the stop one
        else:
            valueList = baselineDictionary.get(word)
    except KeyError:
        valueList = [0,0,0,0,0,0,0,0]
        #do nothing if its not been created we use default tup
    
    if(valueList == None):
        valueList = [0,0,0,0,0,0,0,0]
    
    wordValue = valueList[index]
    wordValue += 1

    valueList[index] = wordValue

    if(Experiment == 1):
        stopWordDictionary[word] = valueList
        ##indicating its the stop one
    else:
        baselineDictionary[word] = valueList
    
    




##driver
##reading in the file

def readInFile(Experiment):
    with open('hns_2018_2019.csv',encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            year = row[9]
            
            print("firstif")
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
                        word = word.strip()
                        wordOutputList.append(word)

                if(year == '2018'):
                    for word in wordOutputList:
                        print("into")
                        addtoDict(word, postType,Experiment)
                
                if(year == '2019' and Experiment == 0):
                    listTuple = [wordOutputList, postType]
                    testingList.append(listTuple)
                
                line_count += 1

        print(f'Processed {line_count} lines.')






def smoothingData(inputDictionary):
    #creating the percentages 
   
    global storyCount
    global askCount
    global showCount
    global pollCount
    smoothingFactor = len(inputDictionary)*0.5


    # Key: freq story, % story, freq ask_hn, % ask Hn, freq show_hn, % show_hn, freq poll, % poll 
    for key in inputDictionary:

        valueList = inputDictionary.get(key)
    
        storyPercent = ((valueList[0]+0.5)/(storyCount+smoothingFactor))
        askPercent = ((valueList[2]+0.5)/(askCount+smoothingFactor))
        showPercent = ((valueList[4]+0.5)/(showCount +smoothingFactor))
        pollPercent = ((valueList[6]+0.5)/(pollCount+smoothingFactor))

        valueList[1] = storyPercent
        valueList[3] = askPercent
        valueList[5] = showPercent
        valueList[7]= pollPercent

        inputDictionary[key] = valueList

    return inputDictionary





    #sorting a list for the output file

def baselineOutput():
    global baselineDictionary
    sortedkeys = []
    for key in baselineDictionary:
        sortedkeys.append(key)

    sortedkeys.sort()

    f = open("model-2018.txt", "w")
    f.truncate(0)
    i = 0
    for key in sortedkeys:
        
        stringtoWrite = str(i) + " " + key + " "
        outputFromDict = baselineDictionary.get(key)
        for value in outputFromDict:
            stringtoWrite = stringtoWrite + " " + str(value)
        #print(stringtoWrite)
        try:
            f.write(stringtoWrite)
        except UnicodeEncodeError:
            print("errror skipping")
            # stringtoWrite = stringtoWrite.encode().decode("utf-8")
            # f.write(stringtoWrite)
        f.write('\n')
        i += 1
    f.close()



def stopWordOutput():
    global stopWordDictionary
    sortedkeys = []
    for key in stopWordDictionary:
        sortedkeys.append(key)

    sortedkeys.sort()

    f = open("stopword-model.txt", "w")
    f.truncate(0)
    i = 0
    for key in sortedkeys:
        
        stringtoWrite = str(i) + " " + key + " "
        outputFromDict =stopWordDictionary.get(key)
        for value in outputFromDict:
            stringtoWrite = stringtoWrite + " " + str(value)
        #print(stringtoWrite)
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


# Key: freq story, % story, freq ask_hn, % ask Hn, freq show_hn, % show_hn, freq poll, % poll 

##task two is to use ML classifier to test the 2019 dataset
##take in array of words and calculate it
##want to return the classifcation and the score of each
def naiveBays(sentance, integer):
    storyScore = 0
    askScore = 0
    showScore = 0
    pollScore = 0
    global baselineDictionary
    global stopWordDictionary

    for word in sentance:
        if integer == 0:
            data = baselineDictionary.get(word)
        if integer == 1:
            data = stopWordDictionary.get(word)
        if(data != None):
            storyScore += math.log10(float(data[1]))
            askScore += math.log10(float(data[3]))
            showScore += math.log10(float(data[5]))
            pollScore += math.log10(float(data[7]))

    values = {'story': storyScore, 'ask_hn': askScore, 'show_hn': showScore, 'poll': pollScore}

    classifcation = max(values, key=values.get)

    outputList = (classifcation,storyScore,askScore,showScore,pollScore)

    return outputList



##function for iterating though the 2019 testing list

def ChecktestingData(integer):
    global testingList

    correct = 0
    wrong = 0
    if integer == 0:
        f = open("baseline-result.txt", "w")
        f.truncate(0)
    if integer == 1:
        f = open("stopword-result.txt", "w")
        f.truncate(0)
    i = 0
    for value in testingList:
        
        sentance = value[0]
        postType = value[1]
        
        outputList = naiveBays(sentance,integer)

        classified = str(outputList[0])
        acutally = str(postType)

        stringtoWrite = str(i) + " " + "classified as: " + classified +  " Acutally " + acutally + " scores: " + str(outputList[1]) + " " + str(outputList[2]) +  " " + str(outputList[3])+  " " + str(outputList[4])

        if classified == acutally:
            correct +=1
        else:
            wrong += 1
    
        try:
            f.write(stringtoWrite)
        except UnicodeEncodeError:
            print("errror skipping")
            # stringtoWrite = stringtoWrite.encode().decode("utf-8")
            # f.write(stringtoWrite)
        f.write('\n')
        i += 1
    f.write("This model Got " + str(correct) + " Correct and " + str(wrong) + " wrong ")
    f.close()






#####driver class

##global variables
baselineDictionary = dict()
testingList = []
storyCount = 0
askCount = 0
showCount = 0
pollCount = 0



readInFile(0)
baselineDictionary = smoothingData(baselineDictionary)
baselineOutput()
ChecktestingData(0)
##passing zero measn that the program will run base
##passing one means that it will run the stopOne






### Experiment one is the stop word filtering

stopWordDictionary = dict()
stopWordList = []

##reseting the counter
storyCount = 0
askCount = 0
showCount = 0
pollCount = 0

f = open("stopwords.txt", "r")

for x in f:
    string = str(x)
    word = re.sub("[, \!?:]+", " ", string)
    res = re.sub(r'\W+', ' ', word)
    if(str(res) != " "):
        word = str(res)
        word = word.lower()
        word = word.strip()
        stopWordList.append(word)


readInFile(1)
stopWordDictionary = smoothingData(stopWordDictionary)
stopWordOutput()
ChecktestingData(1)




print("stopLength", str(len(stopWordDictionary)))
print("baseLenghth", str(len(baselineDictionary)))








