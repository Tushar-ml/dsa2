n = int(input())
arr = list(map(int,input().split()))
q = int(input())
query = list(map(int,input().split()))
sumN = sum(arr)
i = 2
for q in query:
    sumN = i*sumN
    print(sumN)
    i += 1