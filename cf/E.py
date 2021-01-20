import random

tol = 0.000001 #numerical tolerance
max_passes = 1000 #max number of times to iterate over a`s without changing
a = [] #lagrange multipliers for solution
#f(x)=sum(a_i*y_i*K(x_i,x)) + b
indicies = []

n = int(input())
dist = []
y = []
for i in range (n):
    indicies.append(i)
    a.append(0)
    tmp = input().split()
    distI = []
    for j in range (n):
        distI.append(int(tmp[j]))
    dist.append(distI)
    y.append(int(tmp[n]))
c = int(input())

def equals(first, second):
    if (abs(first - second) < tol):
        return True
    else:
        return False

def fx(index, b):
    ans = 0.
    for i in range (n):
        ans = ans + a[i] * y[i] * dist[index][i]
    return ans + b

def svm():
    b = 0 #threshold for solution
    for curPass in range (max_passes):
        random.shuffle(indicies)
        for i in range (n):
            Ei = fx(i, b) - y[i] #it`s f(x) from header
            if (((Ei * y[i] < -tol) and (c > a[i])) or ((Ei * y[i] > tol) and (tol < a[i]))):
                j = indicies[i]
                if ((i == j) or (equals(fx(j, b) - y[j], Ei))):
                    continue
                Ej = fx(j, b) - y[j]
                if (y[i] == y[j]):
                    l = max(0., a[i] + a[j] - c)
                    r = min(c, a[i] + a[j])
                else:
                    l = max(0., a[j] - a[j])
                    r = min(c, a[j] - a[i] + c)
                if (equals(l, r)):
                    continue
                nu = 2 * dist[i][j] - dist[j][j] - dist[i][i]
                if (nu > tol):
                    continue
                ajo = a[j]
                aj = max(min(ajo - y[j] * (Ei - Ej) / nu, r), l)
                aio = a[i]
                ai = aio + y[i] * y[j] * (ajo - aj)
                b1 = b - Ei - y[j] * (aj - ajo) * dist[i][j] - y[i] * (ai - aio) * dist[i][i]
                b2 = b - Ej - y[j] * (aj - ajo) * dist[j][j] - y[i] * (ai - aio) * dist[i][j]
                #if both a at the bounds then all thresholds between b1 and b2 satisfy KKT
                if (aio > 0 and aio < c):
                    b = b1
                elif (ajo > 0 and ajo < c):
                    b = b2
                else:
                    b = (b1 + b2) / 2
                a[i] = ai
                a[j] = aj
    return b

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

ansB = svm()
for i in range(n):
    print(toFixed(a[i], 12))
print(toFixed(ansB, 12))
                
                
        
