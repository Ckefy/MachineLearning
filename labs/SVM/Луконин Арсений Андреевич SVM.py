#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import warnings
warnings.filterwarnings('ignore')
import pandas
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


# In[26]:


tol = 0.000001 #numerical tolerance
max_passes = 100 #max number of times to iterate over a`s without changing
#f(x)=sum(a_i*y_i*K(x_i,x)) + b

#constants
polD = 0
polDs = [2, 3, 4, 5]
gausBetta = 0
gausBettas = [1, 2, 3, 4, 5]
c = 0
cs = [0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]
polK = 0.5 #maybe 1
kernType = 'start'


# In[3]:


table = pandas.read_csv('chips.csv')
table.head()


# In[4]:


nn = len(table)
coordX1 = table['x']
coordX2 = table['y']
yStr = table['class']
vectors = []
y = []
for i in range (nn):
    vectors.append([float(coordX1[i]), float(coordX2[i])])
    if yStr[i] == 'P':
        y.append(1)
    else:
        y.append(-1)


# In[5]:


#dataFrames
tableX = table.values[:, :-1]
tableY = np.vectorize(lambda l: -1 if l == 'N' else 1)(table['class'])


# In[6]:


def dist (first, second):
    if (kernType == 'lin'):
        return np.dot(first, second)
    elif (kernType == 'pol'):
        return np.power(gausBetta * np.dot(first, second) + polK, polD)
    else:
        return np.exp(-gausBetta * np.power(np.linalg.norm(first - second), 2))


# In[7]:


def equals(first, second):
    if (abs(first - second) < tol):
        return True
    else:
        return False


# In[8]:


def fx(index, a, b, n, curVectors, curY):
    ans = 0.
    for i in range (n):
        ans = ans + a[i] * curY[i] * dist(curVectors[index], curVectors[i])
    return ans + b


# In[9]:


def svm(n, curVectors, curY):
    a = [] #lagrange multipliers for solution
    indicies = []
    for i in range (n):
        a.append(0)
        indicies.append(i)
    b = 0 #threshold for solution
    for curPass in range (max_passes):
        random.shuffle(indicies)
        for i in range (n):
            Ei = fx(i, a, b, n, curVectors, curY) - curY[i] #it`s f(x) from header
            if (((Ei * curY[i] < -tol) and (c > a[i])) or ((Ei * curY[i] > tol) and (0 < a[i]))):
                j = indicies[i]
                if ((i == j) or (equals(fx(j, a, b, n, curVectors, curY) - curY[j], Ei))):
                    continue
                Ej = fx(j, a, b, n, curVectors, curY) - curY[j]
                if (curY[i] == curY[j]):
                    l = max(0., a[i] + a[j] - c)
                    r = min(c, a[i] + a[j])
                else:
                    l = max(0., a[j] - a[j])
                    r = min(c, a[j] - a[i] + c)
                if (equals(l, r)):
                    continue
                nu = 2 * dist(curVectors[i], curVectors[j]) - dist(curVectors[j], curVectors[j]) - dist(curVectors[i], curVectors[i])
                if (nu > tol):
                    continue
                ajo = a[j]
                aj = max(min(ajo - curY[j] * (Ei - Ej) / nu, r), l)
                if (equals(ajo, aj)):
                    continue
                aio = a[i]
                ai = aio + curY[i] * curY[j] * (ajo - aj)
                b1 = b - Ei - curY[j] * (aj - ajo) * dist(curVectors[i], curVectors[j]) - curY[i] * (ai - aio) * dist(curVectors[i], curVectors[i])
                b2 = b - Ej - curY[j] * (aj - ajo) * dist(curVectors[j], curVectors[j]) - curY[i] * (ai - aio) * dist(curVectors[i], curVectors[j])
                #if both a at the bounds then all thresholds between b1 and b2 satisfy KKT
                if (aio > 0 and aio < c):
                    b = b1
                elif (ajo > 0 and ajo < c):
                    b = b2
                else:
                    b = (b1 + b2) / 2
                a[i] = ai
                a[j] = aj
    return (a, b)


# In[10]:


def signFx(indexX, a, b, n, curVectors, curY):
    ans = 0.
    for i in range (n):
        ans = ans + a[i] * curY[i] * dist(indexX, curVectors[i])
    return np.sign(ans + b)


# In[11]:


def score():
    model = KFold()
    ans = []
    for train, test in model.split(tableX):
        xTrain = tableX[train]
        yTrain = tableY[train]
        xTest = tableX[test]
        yTest = tableY[test]
        svmModel = svm(len(xTrain), xTrain, yTrain)
        yNow = np.apply_along_axis(lambda curX: signFx(curX, svmModel[0], svmModel[1], len(xTest), xTest, yTest), 1, xTest)
        ans.append(f1_score(yTest, yNow))
    return sum(ans) / len(ans)


# In[12]:





# In[13]:


fscores = [] #score, (a, b), type, c, gausBetta, polD
kernType = 'lin'
for ic in cs:
    c = ic
    ansB = svm(nn, vectors, y)
    fscores.append((score(), ansB, 'lin', c, -1, -1))


# In[14]:


maxi = (-1000, 'start', 0, 0, 0)
for i in range(len(fscores)):
    if (maxi[0] < fscores[i][0]):
        maxi = fscores[i]


# In[15]:


maxi1 = maxi
print (maxi[0])


# In[16]:


fscores = []
kernType = 'gaus'
for igausBetta in gausBettas:
    gausBetta = igausBetta
    for ic in cs:
        c = ic
        ansB = svm(nn, np.asarray(vectors), np.asarray(y))
        fscores.append((score(), ansB, 'gaus', c, gausBetta, -1))


# In[17]:


maxi = (-1000, 'start', 0, 0, 0)
for i in range(len(fscores)):
    if (maxi[0] < fscores[i][0]):
        maxi = fscores[i]


# In[18]:


maxi2 = maxi
print (maxi[0])


# In[27]:


fscores = []
kernType = 'pol'
for igausBetta in gausBettas:
    gausBetta = igausBetta
    for ipolD in polDs:
        polD = ipolD
        for ic in cs:
            c = ic
            ansB = svm(nn, np.asarray(vectors), np.asarray(y))
            fscores.append((score(), ansB, 'pol', c, gausBetta, polD))


# In[33]:


maxi = (-1000, 'start', 0, 0, 0)
for i in range(len(fscores)):
    if (maxi[0] < fscores[i][0]):
        maxi = fscores[i]
# -1 - it`s not used in this type of kernel


# In[34]:


maxi3 = maxi
print (maxi[0])
draw()


# In[31]:


savedMaxi1 = maxi1
savedMaxi2 = maxi2
savedMaxi3 = maxi3


# In[ ]:





# In[ ]:




