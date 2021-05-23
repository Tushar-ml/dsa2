
from collections import defaultdict
def solve(w,wr,arr):
    hashmap = defaultdict(int)
    if wr>=w:
        return 'YES'
        
    else:
        w -= wr
        arr.sort()
        for w in arr:
            hashmap[w] += 1 
        
        for key,value in hashmap.items():
            n = value//2
            w -= n*key
            
    if w<=0:
        return 'YES'
    return 'NO'
    
    
t = int(input())

for _ in range(t):
    n,w,wr = list(map(int,input().split()))
    arr = list(map(int,input().split()))
    res = solve(w,wr,arr)
    print(res)