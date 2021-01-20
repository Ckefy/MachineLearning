import math

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

n = int(input())
xs = []
ys = []
xsum = 0
ysum = 0
for i in range(n):
    x, y = map(int, input().split(' '))
    xs.append(x)
    ys.append(y)
    xsum += x
    ysum += y
xavg = xsum / len(xs)
yavg = ysum / len(ys)
dx = 0
dy = 0
alll = 0
for i in range(n):
    alll += (ys[i] - yavg) * (xs[i] - xavg)
    dx += (xs[i] - xavg) * (xs[i] - xavg)
    dy += (ys[i] - yavg) * (ys[i] - yavg)
if (dx * dy == 0):
    print(0)
else:
    print (toFixed(alll / math.sqrt(dx * dy), 6))
