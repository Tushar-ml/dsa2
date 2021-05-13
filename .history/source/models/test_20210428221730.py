n,k = list(map(int,input().split()))
matrix = [[False for i in range(n)] for j in range(n)]
cellEmpty = n*n
for q in range(k):
    r,c = list(map(int,input().split()))
    cellFilled = 0
    for i in range(n):
        if matrix[r][i] == False:
            cellFilled += 1
            matrix[r][i] = True
        if matrix[i][c] == False:
            cellFilled += 1
            matrix[i][c] = True

    print(cellEmpty - cellFilled)
    print(matrix)
    cellEmpty -= cellFilled



        