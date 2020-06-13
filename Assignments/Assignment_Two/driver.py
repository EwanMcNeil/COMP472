

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
import nltk
import matplotlib.pyplot as plt


plt.ylabel('Accuracy')
plt.xlabel('number of words')

nltk.download('punkt')


##functions
def addtoDict(word, postType, Experiment):
    
    global labelDictionary
    global stopWordList
    global stopWordDictionary
    global baselineDictionary
    index = 0

    if(Experiment == 2):
        wordLength = len(word)
        if(wordLength <= 2 ):
            return
        if(wordLength >= 9 ):
            return


    if(Experiment == 1):
        ##indicating its the stop one
        if (word in stopWordList):
           return
    
    for key in labelDictionary:
        if key == postType:
            data = labelDictionary.get(key)
            data[0] = data[0] + 1
            index = data[1]
            labelDictionary[key] = data

    # #index of the current type
    # if(postType == 'story'):
    #     print("story")
    #     storyCount += 1
    #     index = 0
        
    # if(postType == 'ask_hn'):
    #     askCount += 1
    #     index = 2
        
    # if(postType == 'show_hn'):
    #     showCount += 1
    #     index = 4
        
    # if(postType == 'poll'):
    #     pollCount += 1
    #     index = 6


    
    try:
        if(Experiment == 0):
            valueList = baselineDictionary.get(word)
        ##indicating its the stop one
        if(Experiment == 1):
            valueList = stopWordDictionary.get(word)
        if(Experiment == 2):
            valueList = sizeDictionary.get(word)
          
    except KeyError:
        valueList = [0] * len(labelDictionary) * 2
        #do nothing if its not been created we use default tup
    
    if(valueList == None):
        valueList = [0] * len(labelDictionary) * 2
    

    #here there might be an issue 
    #need to loop to indcrease the list size 
    boolIndexError = True
    while boolIndexError:
        try:
            wordValue = valueList[index]
            wordValue += 1
            valueList[index] = wordValue
            boolIndexError = False 
        except IndexError:
            valueList.append(0)
            valueList.append(0)

    if(Experiment == 0):
        baselineDictionary[word] = valueList
        ##indicating its the stop one
    if(Experiment == 1):
        stopWordDictionary[word] = valueList
    if(Experiment == 2):
        sizeDictionary[word] = valueList


    
    




##driver
##reading in the file

def readInFile(Experiment):
    global labelDictionary
    
    with open('hns_2018_2019.csv',encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        typeCount = 0
        for row in csv_reader:
            year = row[9]
            
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:

                
                postType = row[3]
                #here checking for value
                if not (postType in labelDictionary):
                    ##labelDictionary counts number of words associated, index of the words, number of articals with that one
                    labelDictionary[postType] = [0, typeCount, 0]
                    typeCount += 2

                #here we are adding in the percent of 
                addData = labelDictionary[postType]
                addData[2] = addData[2] + 1
                labelDictionary[postType] = addData


                title = row[2]

                # res = "".join(filter(lambda x: not x.isdigit(), title)) 
                # string = str(res)
                # wordList = re.sub("[, \!?:]+", " ", string).split()

                # wordOutputList = []
                # for word in wordList:
                #     res = re.sub(r'\W+', ' ', word)

                #     if(str(res) != " "):
                #         word = str(res)
                #         word = word.lower()
                #         word = word.strip()
                #         wordOutputList.append(word)

                words = nltk.word_tokenize(title)
                wordOutputList = [word for word in words if word.isalnum()]
                i = 0 
                for word in wordOutputList:
                    wordOutputList[i] = (word.lower()).strip()
                    if(any(char.isdigit() for char in word)):
                       del wordOutputList[i]
                    i += 1

                if(year == '2018'):
                    for word in wordOutputList:
                            addtoDict(word, postType,Experiment)
                
                if(year == '2019' and Experiment == 0):
                    listTuple = [wordOutputList, postType]
                    testingList.append(listTuple)
                
                line_count += 1
        
        for key in labelDictionary:
            DivData = labelDictionary[key]
            DivData[2] = DivData[2]/line_count
            labelDictionary[key] = DivData

        print(f'Processed {line_count} lines.')




def smoothingData(inputDictionary):

    global labelDictionary

    # i = 0
    # ##removing the less useful data
    # for key in inputDictionary:
    #     valueList = inputDictionary.get(key


    #     #if I remove this later remeber to keep this part
        

     

    #     total = 0
    #     for key in labelDictionary:
    #         data = labelDictionary.get(key)
    #         total += valueList[data[1]]
        
    #     if total <= 1:
    #         del inputDictionary[i]
            
    #     i += 1




    #creating the percentages 
   
    # global storyCount
    # global askCount
    # global showCount
    # global pollCount

    
    smoothingFactor = len(inputDictionary)*0.5

    outputDictionary = inputDictionary.copy()

    # Key: freq story, % story, freq ask_hn, % ask Hn, freq show_hn, % show_hn, freq poll, % poll 
    for key in inputDictionary:

        valueList = inputDictionary.get(key)
    
        # storyPercent = ((valueList[0]+0.5)/(storyCount+smoothingFactor))
        # askPercent = ((valueList[2]+0.5)/(askCount+smoothingFactor))
        # showPercent = ((valueList[4]+0.5)/(showCount +smoothingFactor))
        # pollPercent = ((valueList[6]+0.5)/(pollCount+smoothingFactor))

        # valueList[1] = storyPercent
        # valueList[3] = askPercent
        # valueList[5] = showPercent
        # valueList[7]= pollPercent

        ##to account for unseen zeros
        while len(valueList) < (len(labelDictionary)*2):
            valueList.append(0)


        for key in labelDictionary:
            data = labelDictionary.get(key)
            addition = float((valueList[data[1]]+0.5))
            smoothAddition = float((data[0]+smoothingFactor))
            percent =  addition/smoothAddition
            valueList[data[1]+1] = percent

        outputDictionary[key] = valueList

    return outputDictionary

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

        try:
            f.write(stringtoWrite)
        except UnicodeEncodeError:
            print(" ")
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



def sizeWordOutput():
    global sizeDictionary
    sortedkeys = []
    for key in sizeDictionary:
        sortedkeys.append(key)

    sortedkeys.sort()

    f = open("size-model.txt", "w")
    f.truncate(0)
    i = 0
    for key in sortedkeys:
        
        stringtoWrite = str(i) + " " + key + " "
        outputFromDict = sizeDictionary.get(key)
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
    ## need to make local dictionary here
    global labelDictionary

   

    scoreDictionary = dict()

    for key in labelDictionary:
        percentdata = labelDictionary[key]
        scoreDictionary[key] = math.log10(percentdata[2])
    # storyScore = 0
    # askScore = 0
    # showScore = 0
    # pollScore = 0
    global baselineDictionary
    global stopWordDictionary

    for word in sentance:
        if integer == 0:
            if word in baselineDictionary:
             data = baselineDictionary.get(word)
            else:
             data = None 
        if ((integer == 1) or (integer == 3)):
            if word in stopWordDictionary:
             data = stopWordDictionary.get(word)
            else:
             data = None 
        if integer == 2:
            if word in sizeDictionary:
             data = sizeDictionary.get(word)
            else:
             data = None 
        if(data != None):
            for key in scoreDictionary:
                labelInfo = labelDictionary.get(key)
                currentScore = scoreDictionary.get(key)
                currentScore += math.log10((data[labelInfo[1]+1]))
                scoreDictionary[key] = currentScore
                
            # storyScore += math.log10(float(data[1]))
            # askScore += math.log10(float(data[3]))
            # showScore += math.log10(float(data[5]))
            # pollScore += math.log10(float(data[7]))

    # values = {'story': storyScore, 'ask_hn': askScore, 'show_hn': showScore, 'poll': pollScore}

    classifcation = max(scoreDictionary, key=scoreDictionary.get)

    outputList = [classifcation]
    for key in scoreDictionary:
        value = scoreDictionary.get(key)
        outputList.append(key)
        outputList.append(value)

    return outputList



##function for iterating though the 2019 testing list

def ChecktestingData(integer, dictionaryLength, graph, inputString):
    global testingList

    correct = 0
    wrong = 0
    if integer == 0:
        f = open("baseline-result.txt", "w")
        f.truncate(0)
    if integer == 1:
        f = open("stopword-result.txt", "w")
        f.truncate(0)
    if integer == 2:
        f = open("size-result.txt", "w")
        f.truncate(0)
    i = 0
    for value in testingList:
        
        sentance = value[0]
        postType = value[1]
        
        outputList = naiveBays(sentance,integer)

        classified = str(outputList[0])
        acutally = str(postType)
        correctingString = " wrong"

        if classified == acutally:
            correctingString = " right "
            correct +=1
        else:
            wrong += 1

        if integer != 3:
            stringtoWrite = str(i) + " " + "classified as: " + classified +  " Acutally " + acutally + " scores: "
            
            outputindex = 1
            while outputindex < len(outputList):
                stringtoWrite += " " + str(outputList[outputindex])
                outputindex += 1

            stringtoWrite += correctingString
            try:
                f.write(stringtoWrite)
            except UnicodeEncodeError:
                print("errror skipping")
                # stringtoWrite = stringtoWrite.encode().decode("utf-8")
                # f.write(stringtoWrite)
            f.write('\n')
            i += 1
        if integer != 3:     
            f.write("This model Got " + str(correct) + " Correct and " + str(wrong) + " wrong ")
    
    if(graph == True):
        print(str(dictionaryLength),str(correct/(correct+wrong)))
        plt.plot(dictionaryLength,correct/(correct+wrong),'ro')
        plt.annotate(inputString, (dictionaryLength,correct/(correct+wrong)))
    if integer != 3:
        f.close()






#####driver class

##global variables
baselineDictionary = dict()
testingList = []

#since labelDictionary is reused I want to copy it to a new one
baselineFrequencyDict = dict()
labelDictionary = dict()
#uses labels as keys and then counts as values

#need to refactor to a dict



readInFile(0)
baselineDictionary = smoothingData(baselineDictionary)
baselineOutput()
ChecktestingData(0, len(baselineDictionary), True, "Baseline")



##used in experiment three
baseFrequency = dict()
#getting a freqency table from the baseline
for key in baselineDictionary:
    frequency = 0
    values = baselineDictionary[key]
    for innerKey in labelDictionary:
        label = labelDictionary[innerKey]
        index = label[1]
        frequency += values[index]

    baseFrequency[key] = frequency
    



    
##passing zero measn that the program will run base
##passing one means that it will run the stopOne






### Experiment One StopWord Filtering

stopWordDictionary = dict()
stopWordList = []

##reseting the counter
##needs to occur for the stop as well
labelDictionary.clear()

# storyCount = 0
# askCount = 0
# showCount = 0
# pollCount = 0

f = open("stopwords.txt", "r")

for x in f:
    words = nltk.word_tokenize(x)
    new_words= [word for word in words if word.isalnum()]
    i = 0 
    for word in new_words:
        new_words[i] = (word.lower()).strip()
        i += 1
    for word in new_words:
        stopWordList.append(word)


readInFile(1)
stopWordDictionary = smoothingData(stopWordDictionary)
stopWordOutput()
ChecktestingData(1,len(stopWordDictionary), False, " ")




### Experiment Two word size filtering

sizeDictionary = dict()
labelDictionary.clear()
readInFile(2)

sizeDictionary = smoothingData(sizeDictionary)
sizeWordOutput()
ChecktestingData(2, len(sizeDictionary), False, " ")






####Experiment Three
##less than 5

##I think i can reuse the stopWord dictionary for now

#lessFiveDictionary = dict()
stopWordDictionary.clear()
labelDictionary.clear()
stopWordList.clear()


for key in baseFrequency:
    value = baseFrequency[key]
    print(value)
    if value <= 5:
        stopWordList.append(key)


print(stopWordList)
readInFile(1)

stopWordDictionary = smoothingData(stopWordDictionary)

ChecktestingData(3, len(stopWordDictionary), True, "Less than Five")







stopWordDictionary.clear()
labelDictionary.clear()
stopWordList.clear()


for key in baseFrequency:
    value = baseFrequency[key]
    print(value)
    if value <= 10:
        stopWordList.append(key)


print(stopWordList)
readInFile(1)

stopWordDictionary = smoothingData(stopWordDictionary)

ChecktestingData(3, len(stopWordDictionary), True, "Less than Ten")







stopWordDictionary.clear()
labelDictionary.clear()
stopWordList.clear()


for key in baseFrequency:
    value = baseFrequency[key]
    print(value)
    if value <= 20:
        stopWordList.append(key)


print(stopWordList)
readInFile(1)

stopWordDictionary = smoothingData(stopWordDictionary)

ChecktestingData(3, len(stopWordDictionary), True, "Less than 20")

print("sizeLength", str(len(sizeDictionary)))
print("stopLength", str(len(stopWordDictionary)))
print("baseLenghth", str(len(baselineDictionary)))
plt.show()