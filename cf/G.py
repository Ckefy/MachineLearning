import copy
m, k, h = map(int, input().split(' '))
n = int(input())
xs = []
ys = []
data = []
for i in range(n):
    tmp = list(map(int, input().split(' ')))
    data.append(tmp)

countersAll = []
for i in range(k + 1):
        countersAll.append((0, 0))


def bestSplit(data):
    bestInd = 10000
    bestValue = 10000
    bestPure = 10000
    bestLR = None
    for ind in range(len(data[0]) - 1):
        data2 = sorted(data, key = lambda x: x[ind])
        #print(data2)
        for j in range(1):
            if (len(data2) <= 1):
                continue
            obj = data2[j]
            nextObj = data2[j + 1]
            #lr = trySplit(ind, obj, data2)
            if (obj[ind] == nextObj[ind]):
                lr = ([], data2, (obj[ind] + nextObj[ind]) / 2)
            else:
                fst = []
                fst.append(data2[0])
                lr = (fst, data2[1:], (obj[ind] + nextObj[ind]) / 2)
            #print(lr[0], "f", lr[1])
            pure, sum0, n0, sum1, n1, counters = countGini(lr[0], lr[1])
            left = copy.copy(lr[0])
            right = copy.copy(lr[1])
            if bestPure > pure:
                bestPure = pure
                bestInd = ind
                bestValue = lr[2]
                bestLR = (lr[0], lr[1])
            #print(sum0)
            #print(sum1)
            #print(pure)
            for z in range (1, len(data2) - 1):
                while (right[0][ind] * 2 < data2[z][ind] + data2[z + 1][ind]):
                    poped = right.pop(0)
                    left.append(poped)
                    c = poped[-1]
                    
                    sum0 *= (n0 * n0)
                    sum0 += 2 * counters[c][0]
                    sum0 += 1
                    sum0 /= ((n0 + 1) * (n0 + 1))
                    n0 += 1

                    sum1 *= (n1 * n1)
                    sum1 -= 2 * counters[c][1]
                    sum1 += 1
                    sum1 /= ((n1 - 1) * (n1 - 1))
                    n1 -= 1
                    
                    counters[c] = (counters[c][0] + 1, counters[c][1] - 1)
                #print(sum0)
                #print(sum1)
                pure = (1 - sum0) * n0 / (n0 + n1) + (1 - sum1) * n1 / (n0 + n1)
                #print(pure)
                if bestPure > pure:
                    bestPure = pure
                    bestInd = ind
                    bestValue = (data2[z][ind] + data2[z + 1][ind]) / 2
                    bestLR = (copy.copy(left), copy.copy(right))
    return {'index':bestInd, 'value':bestValue, 'lr': bestLR}

def countGini(left, right):
    counters = copy.copy(countersAll)
    children = (left, right)
    ans = 0.0
    indexChild = 0
    allSize = float(sum([len(child) for child in children]))
    summa0 = 0
    n0 = 0
    summa1 = 0
    n1 = 0
    for child in children:
        summa = 0.0
        curSize = float(len(child))
        if curSize == 0:
            indexChild += 1
            continue
        for c in range(1, k + 1):
            curCount = [obj[-1] for obj in child].count(c)
            if (indexChild == 0):
                counters[c] = (counters[c][0] + curCount, counters[c][1])
            else:
                counters[c] = (counters[c][0], counters[c][1] + curCount)
            prob = curCount / curSize
            summa += prob * prob
        ans += (1 - summa) * (curSize / allSize)
        if (indexChild == 0):
            summa0 = summa
            n0 = curSize
            indexChild += 1
        else:
            summa1 = summa
            n1 = curSize
    return ans, summa0, n0, summa1, n1, counters

curID = 1

def countClasses(t):
    if (len(t) > 0):
        fst = t[0]
    else:
        return False
    for obj in t:
        if (obj[-1] != fst[-1]):
            return False
    return True
        

def recurSplit(curNode, curDepth, maxDepth):
    global curID
    curNode['id'] = curID
    curID += 1
    left, right = curNode['lr']
    del(curNode['lr'])
    if not left or not right:
        curNode['l'] = curNode['r'] = (makeLeaf(left + right), curID)
        curID += 1
    elif (maxDepth <= curDepth):
        curNode['l'] = (makeLeaf(left), curID)
        curID += 1
        curNode['r'] = (makeLeaf(right), curID)
        curID += 1
    else:
        if len(left) <= 1:
            curNode['l'] = (makeLeaf(left), curID)
            curID += 1
        else:
            curNode['l'] = bestSplit(left)
            recurSplit(curNode['l'], curDepth + 1, maxDepth)
        if len(left) <= 1:
            curNode['r'] = (makeLeaf(right), curID)
            curID += 1
        else:
            curNode['r'] = bestSplit(right)
            recurSplit(curNode['r'], curDepth + 1, maxDepth)

def makeLeaf(arr):
    freq = [obj[-1] for obj in arr]
    return max(set(freq), key = freq.count)

def build(data, maxDepth):
    root = bestSplit(data)
    recurSplit(root, 1, maxDepth)
    return root

def printTree (curNode):
    if isinstance(curNode, dict):
        left = curNode['l']
        if isinstance(left, dict):
            leftID = left['id']
        else:
            leftID = left[1]
        right = curNode['r']
        if isinstance(right, dict):
            rightID = right['id']
        else:
            rightID = right[1]    
        print("Q", curNode['index'] + 1, curNode['value'], leftID, rightID)
        printTree(curNode['l'])
        printTree(curNode['r'])
    else:
        print("C", curNode[0])

tree = build(data, h)
print(curID - 1)
printTree(tree)
