#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as graphs


# In[2]:


def readXY(index):
    index = str(index)
    if len(index) == 1:
        index = '0' + index
    trainTemp = pd.read_csv("data/" + index + "_" + "train.csv")
    trainX = trainTemp[trainTemp.columns[:-1]].loc[:].values
    trainY = trainTemp[trainTemp.columns[-1]].loc[:].values
    
    testTemp = pd.read_csv("data/" + index + "_" + "test.csv")
    testX = testTemp[testTemp.columns[:-1]].loc[:].values
    testY = testTemp[testTemp.columns[-1]].loc[:].values
    return trainX, trainY, testX, testY


# In[3]:


#https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
n = 21
max_depth = 15
crits = ["gini", "entropy"]
splittings = ["random", "best"]
depths = []
for i in range(max_depth):
    depths.append(i + 1)

bestTrees = []

for i in range(n):
    print("Processing file #", end='')
    print(i + 1)
    maxAcc = 0
    maxParams = ("", "", 0)
    fileIndex = i + 1
    file = readXY(fileIndex) #trainX, trainY, testX, testY
    curTrainX = file[0]
    curTrainY = file[1]
    curTestX = file[2]
    curTestY = file[3]
    for crit in crits:
        for splitting in splittings:
            for depth in depths:
                tree = DecisionTreeClassifier(criterion = crit, splitter = splitting, max_depth = depth)
                tree.fit(curTrainX, curTrainY)
                yPredicted = tree.predict(curTestX)
                yTrue = curTestY
                curAcc = accuracy_score(yTrue, yPredicted)
                if (curAcc > maxAcc):
                    maxAcc = curAcc
                    maxParams = (crit, splitting, depth)
    bestTrees.append((maxAcc, maxParams))


# In[4]:


maxAnsDepth = 0
minAnsDepth = 100
ind = 0
for pair in bestTrees:
    ind += 1
    if (pair[1][2] >= maxAnsDepth):
        maxAnsDepth = pair[1][2]
        treeWithMaxDepth = ind
    if (pair[1][2] <= minAnsDepth):
        minAnsDepth = pair[1][2]
        treeWithMinDepth = ind
print (minAnsDepth, maxAnsDepth)


# # Graphic for tree with min optimal depth

# In[5]:


#only 2 classes
#x = acc, y = depth
minAccsGraph = []
minDepthsGraph = []
file = readXY(treeWithMinDepth) #trainX, trainY, testX, testY
curTrainX = file[0]
curTrainY = file[1]
curTestX = file[2]
curTestY = file[3]
params = bestTrees[treeWithMinDepth - 1][1]
for i in range(50):
    depth = i + 1
    tree = DecisionTreeClassifier(criterion = params[0], splitter = params[1], max_depth = depth)
    tree.fit(curTrainX, curTrainY)
    yPredicted = tree.predict(curTestX)
    yTrue = curTestY
    curAcc = accuracy_score(yTrue, yPredicted)
    minAccsGraph.append(curAcc)
    minDepthsGraph.append(depth)


# In[6]:


graphs.plot(minAccsGraph, minDepthsGraph)
graphs.xlabel('Accuracy')
graphs.ylabel('Depth')
graphs.show()


# # Graphic for tree with max optimal depth

# In[7]:


#x = acc, y = depth
maxAccsGraph = []
maxDepthsGraph = []
file = readXY(treeWithMaxDepth) #trainX, trainY, testX, testY
curTrainX = file[0]
curTrainY = file[1]
curTestX = file[2]
curTestY = file[3]
params = bestTrees[treeWithMaxDepth - 1][1]
for i in range(15):
    depth = i + 1
    tree = DecisionTreeClassifier(criterion = params[0], splitter = params[1], max_depth = depth)
    tree.fit(curTrainX, curTrainY)
    yPredicted = tree.predict(curTestX)
    yTrue = curTestY
    curAcc = accuracy_score(yTrue, yPredicted)
    maxAccsGraph.append(curAcc)
    maxDepthsGraph.append(depth)


# In[8]:


graphs.plot(maxAccsGraph, maxDepthsGraph)
graphs.xlabel('Accuracy')
graphs.ylabel('Depth')
graphs.show()


# In[9]:


forest = []
for i in range(n):
    forest.append([])
    print("Processing file #", end='')
    print(i + 1)
    fileIndex = i + 1
    file = readXY(fileIndex) #trainX, trainY, testX, testY
    curTrainX = file[0]
    curTrainY = file[1]
    curTestX = file[2]
    curTestY = file[3]
    for crit in crits:
        for splitting in splittings:
            tree = DecisionTreeClassifier(criterion = crit, splitter = splitting)
            tree.fit(curTrainX, curTrainY)
            yPredicted = tree.predict(curTestX)
            yTrue = curTestY
            curAcc = accuracy_score(yTrue, yPredicted)
            forest[i].append((curAcc, splitting, crit))


# In[10]:


preTable = []
indeces = []
name1 = forest[0][0][1] + ' & ' + forest[0][0][2]
name2 = forest[0][1][1] + ' & ' + forest[0][1][2]
name3 = forest[0][2][1] + ' & ' + forest[0][2][2]
name4 = forest[0][3][1] + ' & ' + forest[0][3][2]
for i in range(n):
    indeces.append(i + 1)
    preTable.append([forest[i][0][0], forest[i][1][0], forest[i][2][0], forest[i][3][0]])
table = pd.DataFrame(preTable, index = indeces, columns = [name1, name2, name3, name4])
table


# In[ ]:




