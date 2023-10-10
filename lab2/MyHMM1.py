import sys
# pypy3 MyHMM0.py < test.in

def vectorMul(A, B, colnum):
    alpha = []

    for i in range(len(A)):
        alpha.append(A[i] * B[i][colnum])
    print(alpha)
    return alpha

def forward(seq, A, B, pi):
    alpha = vectorMul(pi[0], B, seq[0])

    a = []
    elem = 0
    for state in seq:
        for i in range(len(alpha)):
            for j in range(len(A[0])):
                elem += alpha[j] * A[j][i]
            a.append(elem)
        alpha = vectorMul(a, B, state)
   # print(a)

def matrixMultiplication(A, B):

    result = []
    for i in range(len(A)):
        for j in range(len(B[0])):
            element_val = 0
            for k in range(len(A[0])):
                #print(float(A[i][k]))
                element_val += A[i][k] * B[k][j]
            result.append(element_val)
            
    return result

pi = []
A = []
B = []
seq = []
linecount = 0
for line in sys.stdin:
    line = line.split()
    if linecount == 3:
        num_elem = int(line[0])
        for i in range(num_elem):
            seq.append(int(line[i+1]))
    row, col = int(line[0]), int(line[1])
    for i in range(row):
        rowelem = []
        for j in range(col):
            rowelem.append(float(line[i*col + j + 2]))
        if linecount==0:
            B.append(rowelem)
        if linecount==1:
            A.append(rowelem)
        if linecount==2:
            pi.append(rowelem)
    linecount+=1

forward(seq, A, B, pi)


    
