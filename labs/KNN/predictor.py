from enum import Enum
import math 

class enumMetric(Enum):
    MAN = "manhattan"
    EU = "euclidean"
    CH = "chebyshev"
 
class enumKern(Enum):
    UN = "uniform"
    TRIA = "triangular"
    EP = "epanechnikov"
    QUAR = "quartic"
    TRIW = "triweight"
    TRIC = "tricube"
    GAU = "gaussian"
    COS = "cosine"
    LOG = "logistic"
    SIG = "sigmoid"
 
class enumWindow(Enum):
    FIX = "fixed"
    VAR = "variable"
 
def dist(first, second):
    ans = 0
    if curMetric == curMetric.MAN:
        for i in range(m):
            ans += abs(first[i] - second[i])
    elif curMetric == curMetric.EU:
        for i in range(m):
            ans += abs(first[i] - second[i]) ** 2
        ans = math.sqrt(ans)
    else:
        ans -= 1
        for i in range(m):
            ans = max(ans, abs(first[i] - second[i]))
    return ans
 
def sort():
    lst = []
    for i in range(n):
        lst.append((vectors[i], preclass[i], dist(needvec, vectors[i])))
    return sorted(lst, key=lambda i: i[2])
 
def noneighbours():
    tmp1 = []
    for i in range(class_length):
        tmp1.append(0)
    for i in range(n):
        for j in range(class_length):
            tmp1[j] += distances[i][1][j]
    for j in range(class_length):
        tmp1[j] /= n
    return tmp1
 
def K(win, dis):
    u = dis / win
    if abs(u) >= 1:
        if (curKern == enumKern.UN) or (curKern == enumKern.TRIA) or (curKern == enumKern.EP) or (curKern == enumKern.QUAR) or (curKern == enumKern.TRIW) or (curKern == enumKern.TRIC) or (curKern == enumKern.COS):
            return 0
        elif (curKern == enumKern.GAU):
            return (1 / (math.sqrt(2 * math.pi))) * math.exp((-1 / 2) * (u ** 2))
        elif (curKern == enumKern.LOG):
            return 1 / (math.exp(u) + 2 + math.exp(-u))
        else:
            return (2 / math.pi) * 1 / (math.exp(u) + math.exp(-u))      
    else:
        if (curKern == enumKern.UN):
            return 1 / 2
        elif (curKern == enumKern.TRIA):
            return 1 - u
        elif (curKern == enumKern.EP):
            return (3 / 4) * (1 - (u ** 2))
        elif (curKern == enumKern.QUAR):
            return (15 / 16) * ((1 - (u ** 2)) ** 2)
        elif (curKern == enumKern.TRIW):
            return (35 / 32) * ((1 - (u ** 2)) ** 3)
        elif (curKern == enumKern.TRIC):
            return (70 / 81) * ((1 - (u ** 3)) ** 3)
        elif (curKern == enumKern.COS):
            return (math.pi / 4) * math.cos(math.pi * u / 2)
        elif (curKern == enumKern.GAU):
            return (1 / (math.sqrt(2 * math.pi))) * math.exp((-1 / 2) * (u ** 2))
        elif (curKern == enumKern.LOG):
            return 1 / (math.exp(u) + 2 + math.exp(-u))
        else:
            return (2 / math.pi) * 1 / (math.exp(u) + math.exp(-u))
    
def Nadarai():
    tmp1 = []
    for i in range(class_length):
        tmp1.append(0)
    tmp2 = 0
    for i in range(n):
        for j in range(class_length):
            tmp1[j] += distances[i][1][j] * K(h, distances[i][2])
        tmp2 += K(h, distances[i][2])
    first = tmp1
    second = tmp2
    return (first, second)

def predict(_n, _m, _vectors, _preclass, _target, _curMetric, _curKern, _curWindow, _h):
    global n
    n = _n
    global m
    m = _m
    global vectors
    vectors = _vectors
    global preclass
    preclass = _preclass
    global class_length
    class_length = len(preclass[0])
    global needvec
    needvec = _target
    global curMetric
    curMetric = _curMetric
    global curKern
    curKern = _curKern
    global curWindow
    curWindow = _curWindow
    global h
    h = _h
    global distances
    distances = sort()
    if (curWindow == enumWindow.VAR):
        h = distances[h][2]
    if ((h == 0 and (needvec != distances[0][0])) or (h > 0 and Nadarai()[1] == 0)):
        return (noneighbours())
    elif (h == 0):
        ind = 0
        tmp1 = []
        for i in range(class_length):
            tmp1.append(0)
        while ((ind < n) and needvec == distances[ind][0]):
            for i in range(class_length):
                tmp1 += distances[ind][1]
            ind += 1
        for i in range(class_length):
            tmp1 /= ind
        return tmp1
    else:
        pairKern = Nadarai()
        tmp1 = []
        for i in range(class_length):
            tmp1.append(pairKern[0][i]/pairKern[1])
        return tmp1
