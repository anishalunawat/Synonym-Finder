from collections import OrderedDict

inputList = []
inputDict = {}
outputDict = {}
synonymDict = {}

def getInputFromFile():
    myFile = open("sample.csv", "r")
    for line in myFile:
        inputList.append(line.split(","))
    myFile.close()
    
    
def getFrequency():
    for termString in inputList:
        term1 = termString[0]
        term2 = termString[1]
        coOcc = (float)( termString[2].replace('\n',""))
        
        if inputDict.has_key(term1):
            value = inputDict.get(term1) + coOcc
            inputDict[term1] = value
        else:
            inputDict[term1] = coOcc
            
        if inputDict.has_key(term2):
            value = inputDict.get(term2) + coOcc
            inputDict[term2] = value
        else:
            inputDict[term2] = coOcc
            
def getCoOcc(query):
    for terms in inputList:
        term1 = terms[0]
        term2 = terms[1]
        coOcc = (int)(terms[2].replace('\n',""))
        
        if query == term1:
            score = 2 * coOcc / (inputDict.get(term1) + inputDict.get(term2))
            outputDict[term2] = score
        elif query == term2:
            score = 2 * coOcc / (inputDict.get(term1) + inputDict.get(term2))
            outputDict[term1] = score
            

def getSynonyms(query):
    getCoOcc(query)
    for terms in inputList:
        term1 = terms[0]
        term2 = terms[1]
        coOcc = (int)(terms[2].replace('\n',""))
        if term1 != query and term2 != query:
            count1 = inputDict.get(term1)
            count2 = inputDict.get(term2)
            score = 2 * coOcc / (count1 + count2)
            if outputDict.has_key(term1):
                preScore = outputDict.get(term1)
                score = preScore * score
                synonymDict[term2] = score
            if outputDict.has_key(term2):
                preScore = outputDict.get(term2)
                score = preScore * score
                synonymDict[term1] = score
        
        
def run():
    getInputFromFile()
    getFrequency()
    getSynonyms("human")
    #print inputList
    #print inputDict
    #print outputDict
    #synonymDict = sorted(synonymDict.values())
    #synonymDict = synonymDict.reverse()
    synonymDict2 = OrderedDict(sorted(synonymDict.items(), key=lambda kv: kv[1], reverse=True))
    #print synonymDict2
    outputFile = open("output.txt", "w")
    for items in synonymDict2:
        outputFile.write(items + "   " + str(synonymDict2[items]) + "\n")
        print items
    #print "hello"
    outputFile.close()
    
    
run()
#    inputList = myFile.readline()

#print inputList[1][2]
