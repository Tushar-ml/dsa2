n = int(input())
arr = list(map(int,input().split()))
q = int(input())
query = list(map(int,input().split()))
sumN = sum(arr)

for q in query:
    sumN = 2*sumN
    print(sumN)
    i += 1