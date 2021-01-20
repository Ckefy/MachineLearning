n = int(input())
confussion_matrix = []
alll = 0
#c[i,j] = number of objects with class i that recognized as j
for i in range(n):
    confussion_matrix.append([])
    tmp = input().split()
    for j in range (n):
        alll += int(tmp[j])
        confussion_matrix[i].append(int(tmp[j]))
                     
#recall = TP/P
#precision = TP/(TP+FP)

def recall(now):
    p = 0
    for i in range(n):
        p += confussion_matrix[now][i] #all objects from current class
    if p != 0:
        return confussion_matrix[now][now] / p #TP / P
    else:
        return 0

def precision(now):
    tpfp = 0
    for i in range(n):
        tpfp += confussion_matrix[i][now] #all objects recognized as current class
    if tpfp != 0:
        return confussion_matrix[now][now] / tpfp #TP /(TP+FP)
    else:
        return 0

def objfromclass(now):
    p = 0
    for i in range(n):
        p += confussion_matrix[now][i] #all objects from current class
    return p

def f(now):
    if (recall(now) + precision(now)) != 0:
        return 2 * recall(now) * precision(now) / (recall(now) + precision(now))
    else:
        return 0

def fmacro():
    #fmacro = harmonic between PrecW and RecallW
    recallW = 0
    for i in range (n):
        recallW += objfromclass(i) * recall(i)
    recallW /= alll
    precisionW = 0
    for i in range (n):
        precisionW += objfromclass(i) * precision(i)
    precisionW /= alll
    if (recallW + precisionW) != 0:
        return 2 * recallW * precisionW / (recallW + precisionW)
    else:
        return 0

def fmicro():
    #weighted because of muli-class
    #fmicro = sum(c)(C(c) * F(c))/All)
    tmp = 0
    for i in range (n):
        tmp += objfromclass(i) * f(i)
    return tmp / alll

print (fmacro())    
print (fmicro())
