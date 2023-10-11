import sys

# pypy3 MyHMM1.py < test.in

def vectorMul(A, B, colnum):
    alpha = []
    for i in range(len(A)):
        alpha.append(float(A[i]) * float(B[i][colnum]))
    return [alpha]

def matrixMultiplication(alpha, A):
    row, col = len(A), len(A[0])
    result = []
    for j in range(col):
        element_val = 0
        for k in range(row):
            element_val += float(alpha[0][k]) * float(A[k][j])
        result.append(element_val)
    return [result]

def forward(seq, A, B, alpha):
    if len(seq) == 0:
        return alpha

    alpha = matrixMultiplication(alpha, A) #2d
    alpha = vectorMul(alpha[0], B, seq[0]) #1d
    return forward(seq[1:], A, B, alpha)

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

    N, K = int(line[0]), int(line[1])
    if linecount==0:
        for i in range(N):
            A.append(line[i*N + 2:i*N+N+2])
    if linecount==1:
        for i in range(N):
            B.append(line[i*K + 2:(i+1)*K+2])

    if linecount==2:
        pi.append(line[2:K+2])
    linecount+=1

alpha_init = vectorMul(pi[0], B, seq[0])
probability = forward(seq[1:], A, B, alpha_init)
summa = sum(probability[0])
print(summa)