def MxM(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j] 
    return result

def Mn(p):
    matrix = [
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
    ]
    result = [[1 if i == j else 0 for j in range(10)] for i in range(10)]
    for _ in range(p):
        result = MxM(result, matrix)
    return result

def printm(Matrice):
    for row in Matrice:
        print(' '.join(f'{val:3d}' for val in row))

n=int(input("Entre la puissance n = ")) 
printm(Mn(n))