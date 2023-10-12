import sys

def alpha_p(pi, A, B, seq):  
    N = len(A) 
    c_0 = 0
    alpha = []
    for i in range(N):
        alpha_init = float(pi[0][i]) * float(B[i][seq[0]])
        c_0 += alpha_init
        alpha.append(alpha_init)
    # scale alpha_0(i)
    c_0 = 1/c_0
    for i in range(N):
        alpha[i] = alpha[i]*c_0

    c_T = []
    for t in range(1, len(seq)):
        c_t = 0
        for i in range(N):
            alpha_t = 0
            for j in range(N):
                alpha_t = alpha[t] + alpha[t-1]*float(A[j][i])
                alpha.append(alpha_t)
            alpha_t = float(alpha[i]) * float(B[i][seq[t]])
            c_t = c_t + alpha[i]
        # scale alpha_t(i)
        c_t = 1/c_t
        for i in range(N):
            alpha[i] = c_t * alpha[i]
        c_T.append(c_t)
    return alpha , c_T

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

N = len(A)
maxiter = 50
iters = 0
oldLogProb = float("-inf")

# compute alpha-pass
alpha, c_T = alpha_p(pi, A, B, seq)

#init beta
"""beta = []
for i in range(N):
    beta.append(c_T[0])

for t in range(T-2, -1, -1):
    for i in range(N):
        beta[]"""
#    
#seqlength = len(seq)-1
#while seqlength >= 0:
 #   for i in range(N):
        


