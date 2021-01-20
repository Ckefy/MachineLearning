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
for i in range(max(k1, k2)):
    xsum.append(0)
    ysum.append(0)
experiments = {}
for i in range (n):
    xsum[xs[i]] += 1
    ysum[ys[i]] += 1
    experiments[(xs[i], ys[i])] = experiments.get((xs[i], ys[i]), 0) + 1
for i in range(k1):
    xsum[i] /= n
for i in range(k2):
    ysum[i] /= n
ans = n
for e in experiments.keys():
    curE = n * ysum[e[1]] * xsum[e[0]]
    ans += ((experiments[e] - curE) ** (2)) / curE
    ans -= curE
print(ans)
