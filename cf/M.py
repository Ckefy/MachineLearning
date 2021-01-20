import math

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

n = int(input())
xs = []
ys = []
for i in range(n):
    x, y = map(int, input().split(' '))
    xs.append((x, i))
    ys.append((y, i))
xs.sort()
ys.sort()
rankX = []
rankY = []
for i in range(n):
    rankX.append(0)
    rankY.append(0)
for i in range(n):
    indexx = xs[i][1]
    indexy = ys[i][1]
    rankX[indexx] = i
    rankY[indexy] = i
ans = 0
for i in range(n):
    ans += (rankY[i] - rankX[i]) * (rankY[i] - rankX[i])
ans = 1 - ans / (n * n * n - n) * 6
print (ans)
