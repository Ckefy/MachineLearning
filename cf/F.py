import math

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

K = int(input())
lc = []
for i in input().split():
    lc.append(int(i))
a = int(input())
N = int(input())
countWordInClassMap = [] #does the word was used in certain class
countClass = [] #how much time this class appear
for i in range(K):
    countWordInClassMap.append({})
    countClass.append(0)
for i in range(N):
    tempInput = input().split()
    clazz = int(tempInput[0])
    strings = []
    for j in range(len(tempInput) - 2):
        strings.append(tempInput[j + 2])
    clazz -= 1
    countClass[clazz] += 1
    for string in set(strings):
        if not(string in countWordInClassMap[clazz]):
            countWordInClassMap[clazz][string] = 0
        countWordInClassMap[clazz][string] += 1
#stop trains, begin tests
pClass = []
#ln(a / b) = ln(a) - ln(b) - for more accuracy we will
#store division like tuple (a, b)
allSet = set()
for i in range(K):
    for string in countWordInClassMap[i].keys():
        allSet.add(string)

for i in range(K):
    pClass.append({})
    for string in allSet:
        Q = 2 #len(countWordInClassMap[i])
        if not(string in countWordInClassMap[i]):
            countX = 0
        else:
            countX = countWordInClassMap[i][string];
        pClass[i][string] = ((countX + a), (countClass[i] + a * Q))

#print(pClass)

M = int(input())
for i in range(M):
    tempInput = input().split()
    strings = set()
    for j in range(len(tempInput) - 1):
        strings.add(tempInput[j + 1])
    answer = []
    for j in range(K):
        if (countClass[j] == 0):
            answer.append((math.inf, math.inf))
            continue;
        answer.append((math.log(lc[j]), math.log(N)))
        answer[j] = (answer[j][0] + math.log(countClass[j]), answer[j][1])
        for string in strings:
            if not(string in allSet):
                continue
            else:
                if (string in pClass[j]):
                    tempAnswer0 = answer[j][0] + math.log(pClass[j].get(string, 0)[0])
                    tempAnswer1 = answer[j][1] + math.log(pClass[j].get(string, 0)[1])
                    answer[j] = (tempAnswer0, tempAnswer1)
                else:
                    #when countWordInClassMap[][] == 0
                    Q = 2 #len(countWordInClassMap[j])
                    tempAnswer0 = answer[j][0] + math.log(a)
                    tempAnswer1 = answer[j][1] + math.log(countClass[j] + a * Q)
                    answer[j] = (tempAnswer0, tempAnswer1)
        for string in allSet:
            if not(string in strings):
                if (string in pClass[j]):
                    tempAnswer0 = answer[j][0] + math.log(pClass[j].get(string, 0)[1] - pClass[j].get(string, 0)[0])
                    tempAnswer1 = answer[j][1] + math.log(pClass[j].get(string, 0)[1])
                    answer[j] = (tempAnswer0, tempAnswer1)
                else:
                    #when countWordInClassMap[][] == 0
                    Q = 2 #len(countWordInClassMap[j])
                    tempAnswer0 = answer[j][0] + math.log(countClass[j] + a * Q - a)
                    tempAnswer1 = answer[j][1] + math.log(countClass[j] + a * Q)
                    answer[j] = (tempAnswer0, tempAnswer1)
    answerWithoutLn = []
    allAnswer = 0

    average = 0
    Knotnull = 0
    for j in range(K):
        if (answer[j][0] == math.inf):
            continue;
        Knotnull += 1
        lna = answer[j][0]
        lnb = answer[j][1]
        average += (lna - lnb)
    average /= Knotnull
    
    for j in range(K):
        if (answer[j][0] == math.inf):
            answerWithoutLn.append(-1)
            continue;
        lna = answer[j][0]
        lnb = answer[j][1]
        answerWithoutLn.append(math.exp(lna - lnb - average))
        allAnswer += answerWithoutLn[j]
    for j in range(K):
        if (answerWithoutLn[j] == -1):
            print(0)
            continue
        print(toFixed(answerWithoutLn[j] / allAnswer, 10), end = ' ')
    print('')
#p(c|emu dog fish dog fish) = p(c)*p(emu|c)*p(dog|c)*p(fish|c)*(1 - p(ant|c))*(1 - p(bird|c))
#2 class: 1/4 * 1/3 * 2/3 * 2/3 * (1 - 1/3) * (1 - 1/3)
#1 class: 2/4 * 1/4 * 1/2 * 1/2 * 1/2 * 1/4
#3 class: 1/4 * 1/3 * 1/3 * 1/3 * 2/3 * 1/3
