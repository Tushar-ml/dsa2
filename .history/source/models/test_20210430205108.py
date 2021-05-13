
from collections import defaultdict
comb = []
def subset_sum(numbers, target, partial=[]):
    s = sum(partial)

    # check if the partial sum is equals to target
    if s == target: 
        comb.append(partial)
    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, partial + [n]) 

def solve(w,wr,arr):
    hashmap = defaultdict(int)
    if wr>=w:
        return 'YES'
        
    else:
        w -= wr
        
        subset_sum(arr,w)
        print(comb)
        for c in comb:
            flag = True
            hashmap = defaultdict(int)
            for a in c:
                hashmap[a] += 1

            for key,value in hashmap.items():
                if value%2 != 0:
                    flag = False
                    return 'NO'
            if flag:
                return 'YES'
            
    if w<=0:
        return 'YES'
    return 'NO'
    
    
t = int(input())

for _ in range(t):
    n,w,wr = list(map(int,input().split()))
    arr = list(map(int,input().split()))
    res = solve(w,wr,arr)
    print(res)