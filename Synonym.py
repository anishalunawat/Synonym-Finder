import numpy as np

inputList = []
inputDict = {}
outputDict = {}
countThreshold = 3
threshold = 0.0003
VertexList = []
EdgeList = []
theta = 0.0003

outputFile = open("output2.txt", "w")

def getInputFromFile():
    myFile = open("wiki2006.csv", "r")
    for line in myFile:
        inputItem = line.split(",")
        inputItem[2] = float(inputItem[2].replace("\n", ""))
        if inputItem[2] > countThreshold:
            inputList.append(inputItem)
    myFile.close()
    
    
def getFrequency():
    getInputFromFile()
    for termString in inputList:
        term1 = termString[0]
        term2 = termString[1]
        coOcc = termString[2]
        
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
        coOcc = terms[2]
        
        if query == term1:
            score = 2 * coOcc / (inputDict.get(term1) + inputDict.get(term2))
            if score >= threshold:
                outputDict[term2] = score
        elif query == term2:
            score = 2 * coOcc / (inputDict.get(term1) + inputDict.get(term2))
            if score >= threshold:
                outputDict[term1] = score
            

def getSimilarWords(query):
    getCoOcc(query)
    synonymDict = {}
    for term in inputList:
        term1 = term[0]
        term2 = term[1]
        coOcc = term[2]
        if term1 != query and term2 != query:
            count1 = inputDict.get(term1)
            count2 = inputDict.get(term2)
            score = 2 * coOcc / (count1 + count2)
            if outputDict.has_key(term1):
                preScore = outputDict.get(term1)
                preScore = preScore * score
                synonymDict[term2] = preScore
            if outputDict.has_key(term2):
                preScore = outputDict.get(term2)
                preScore = preScore * score
                synonymDict[term1] = preScore
    
    for term in synonymDict:        
        score = synonymDict.get(term)
        if outputDict.has_key(term):
            score = outputDict.get(term) + score
        if score >= threshold:  
            outputDict[term] = score
        
def search(term1, term2):
    startInd = 0
    endInd = len(inputList) - 1
    while startInd <= endInd:
        mid = startInd + int((endInd - startInd) // 2)
        if term1 == inputList[mid][0] and term2 == inputList[mid][1]:
            return inputList[mid][2]
        if term1 < inputList[mid][0]:
            endInd = mid - 1
        elif term1 > inputList[mid][0]:
            startInd = mid + 1
        else:
            if term2 < inputList[mid][1]:
                endInd = mid - 1
            elif term2 > inputList[mid][2]:
                startInd = mid + 1 
    return 0
        
            
def createGraph():
    for term1 in outputDict:
        for term2 in outputDict:
            if term1 != term2:
                coOcc = search(term1, term2)
                count1 = inputDict[term1]
                count2 = inputDict[term2]
                score = 2 * coOcc / (count1 + count2)
                if score > theta: 
                    edge = [term1, term2, score]
                    EdgeList.append(edge)
            
    
def getVertexList():
    createGraph()
    vertexMap = {}
    for edge in EdgeList:
        vertexMap[edge[0]] = edge[0]
        vertexMap[edge[1]] = edge[1]
    for v in vertexMap:
        VertexList.append(v)                    


def getClusters():
    getVertexList()
    vertexMap = {}
    i = 1
    for vert in VertexList:
        vertexMap[vert] = i
        i = i + 1

    flag = 10
    while flag > 0:
        VertexList2 = np.random.permutation(VertexList)
        for vert in VertexList2:
            clusterMap = {}
            maxV = -1
            classV = vertexMap[vert]
            for vert2 in VertexList:
                if vert != vert2:
                    for edge in EdgeList:
                        if edge[0] == vert and edge[1] == vert2:
                            score = edge[2]
                            clusterNo = vertexMap[vert2]
                            if clusterMap.has_key(clusterNo):
                                val = clusterMap.get(clusterNo) + score
                                clusterMap[clusterNo] = val
                            else:
                                clusterMap[clusterNo] = score
            for cl in clusterMap:
                if clusterMap[cl] > maxV:
                    maxV = clusterMap[cl]
                    classV = cl
            
            if vertexMap[vert] != classV:
                flag = flag - 1
                vertexMap[vert] = classV
            
            
    for k, v in sorted(vertexMap.items(), key=lambda kv: kv[1]):
        outputFile.write("%s => %s" % (k,v))
        print("%s => %s" % (k,v))
        

def run():
    getFrequency()
    getSimilarWords("company")
    getClusters()
    outputFile.close()
run()
