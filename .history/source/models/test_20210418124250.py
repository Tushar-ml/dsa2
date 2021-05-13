from collections import defaultdict
m = int(input())
p = int(input())

inmatrix1 = []
inmatrix2 = []

for row in range(m):
    arr = list(map(int,input().split()))
    inmatrix1.append(arr)

for row in range(p):
    arr = list(map(int,input().split()))
    inmatrix2.append(arr)

outmatrix = inmatrix1.copy()

def isSafe(i,j,m,n):
    if i>=0 and i<m and j>=0 and j<n:
        return True
    return False

for row in range(len(inmatrix1)):
    for col in range(len(inmatrix1[0])):
        hashmap = defaultdict(int)
        positions = [(row,row),(row,col),(col,col),(col,row)]
        
        for pos in positions:
            if isSafe(pos[0],pos[1],len(inmatrix2),len(inmatrix2[0])):
                value = inmatrix1[row][col]*inmatrix2[pos[0]][pos[1]]
                hashmap[value] += 1
        
        items = list(hashmap.items())
        
        if not items:
            outmatrix[row][col] = -1
            continue
        items.sort(key=lambda x:(x[1],x[0]),reverse=True)
        print(items)
        if items[0][1]>1:
            outmatrix[row][col] = items[0][0]
        else:
            items.sort(key=lambda x:x[0])
            outmatrix[row][col] = items[0][0]

for i in range(len(outmatrix)):
    for j in range(len(outmatrix[0])):
        print(outmatrix[i][j],end=' ')
    print()


