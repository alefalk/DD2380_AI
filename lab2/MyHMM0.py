import sys
# pypy3 MyHMM0.py < test.in

def matrixMultiplication(A, B):

    result = []
    for i in range(len(A)):
        for j in range(len(B[0])):
            element_val = 0
            for k in range(len(A[0])):
                #print(float(A[i][k]))
                element_val += float(A[i][k]) * float(B[k][j])
            result.append(element_val)
            
    return result

pi = []
A = []
B = []
linecount = 0
for line in sys.stdin:
    line = line.split()
    row, col = int(line[0]), int(line[1])
    for i in range(row):
        rowelem = []
        for j in range(col):
            rowelem.append(line[i*col + j + 2])
        if (linecount==0):
            B.append(rowelem)
        if (linecount==1):
            A.append(rowelem)
        if (linecount==2):
            pi.append(rowelem)
    linecount+=1

result1=[]
result1.append(matrixMultiplication(pi, B))
result2= matrixMultiplication(result1, A)
print(1, len(result2), *result2)


    
