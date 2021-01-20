def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"
 
M = int(input())
 
ans = []
for i in range (1 << M):
    temp = int(input())
    ans.append(temp)
 
print(2)
print(1 << M, 1)
for curMask in range (1 << M):
    for index in range (M):
        if ((1 << index) and curMask):
            print("1.0", end = ' ')
        else:
          print("-11.0", end = ' ')
    print (toFixed(0.5 - bin(curMask).count("1"), 12))
 
for i in ans:
    print (toFixed(ans[i], 12), end = ' ')
print ("-0.5")
