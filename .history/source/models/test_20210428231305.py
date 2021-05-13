n,k = list(map(int,input().split()))
matrix = [[False for i in range(n)] for j in range(n)]
cellEmpty = n*n
for q in range(k):
    r,c = list(map(int,input().split()))
    cellFilled = 0
    for i in range(n):
        if matrix[r-1][i] == False:
            cellFilled += 1
            matrix[r-1][i] = True
        if matrix[i][c-1] == False:
            cellFilled += 1
            matrix[i][c-1] = True

    print(cellEmpty - cellFilled)
    cellEmpty -= cellFilled



        