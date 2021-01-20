import math
k1, k2 = map(int, input().split(' '))
n = int(input())
xs = []
ys = []
for i in range(n):
    x, y = map(int, input().split(' '))
    xs.append(x - 1)
    ys.append(y - 1)
xsum = []
ysum = []
p1 = []
for i in range(k1):
    p1.append(0)
experiments = {}
for i in range (n):
    p1[xs[i]] += 1 / n
    experiments[(xs[i], ys[i])] = experiments.get((xs[i], ys[i]), 0) + 1 / n
ans = 0
for e in experiments.keys():
    curP = experiments[e] / p1[e[0]]
    ans += math.log(curP) * experiments[e] * (-1)
print(ans)
