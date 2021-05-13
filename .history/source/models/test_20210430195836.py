# cook your dish here

def solve(s):
    res = [0]*len(s)
    if s[0] == '0':
        res[0] = -1
    else:
        res[0] = 1 
    hashmap = {'0':0,'1':0}
    for i in range(1,len(s)):
        if s[i] == '0':
            res[i] = res[-1]-1
            hashmap[s[i]] += 1
        else:
            res[i] = res[-1]+1 
            hashmap[s[i]] += 1
        if res[i] == 0:
            return 'YES'
    print(res,hashmap)
    if hashmap['1'] >= hashmap['0']:
        return 'YES'
    return 'NO'

t = int(input())

for _ in range(t):
    l = int(input())
    s = input().strip()
    
    res = solve(s)
    print(res)