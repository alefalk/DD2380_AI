import sys
import math

def alpha_p(pi, A, B, seq):  
    N = len(A) 
    c_0 = 0
    alpha_0 = []
    c_T = []
    for i in range(N):
        alpha_init = float(pi[0][i]) * float(B[i][seq[0]])
        c_0 += alpha_init
        alpha_0.append(alpha_init)
    # scale alpha_0(i)
    c_0 = 1/c_0
    c_T.append(c_0)
    for i in range(N):
        alpha_0[i]= alpha_0[i]*c_0

    alpha_t_matrix = []
    alpha_t_matrix.append(alpha_0)
    for t in range(1, len(seq)):
        alpha_t = []
        c_t = 0
        for i in range(N):
            alpha = 0
            for j in range(N):  
                alpha += float(alpha_t_matrix[t-1][j])*float(A[j][i])
            alpha = alpha * float(B[i][seq[t]])
            alpha_t.append(alpha)
            c_t += alpha

        c_t = 1/c_t
        for i in range(N):
            alpha_t[i] = c_t * alpha_t[i]
        c_T.append(c_t)
        alpha_t_matrix.append(alpha_t)
    return alpha_t_matrix , c_T

def beta_p(A, B, seq, c_T): 
    N = len(A)
    T = len(c_T)
    beta_0 = []
    beta_t_matrix = []

    for _ in range(N):
        beta_0.append(c_T[0])
    beta_t_matrix.append(beta_0)
    for t in range(1,T):
        beta_t = []
        for i in range(N):
            beta = 0
            for j in range(N):
                beta += float(A[i][j])*float(B[j][seq[t-1]])*beta_t_matrix[t-1][j]
            beta_t.append(c_T[t]*beta)
        beta_t_matrix.append(beta_t)
    return beta_t_matrix[::-1]

def gamma(A, B, alpha, beta, seq):
    T = len(alpha)
    N = len(A)
    gamma_i_matrix = []
    gamma_ij_matrix = []
    for t in range(T-1):
        gamma_i_t = []
        gamma_ij_t = []
        for i in range(N):
            gamma_i = 0
            gamma_ij = 0
            gamma_ij_temp = []
            for j in range(N):
                #γt(i, j) = (αt(i)aij bj (Ot+1)βt+1(j))
                #γt(i) = γt(i) + γt(i, j)
                gamma_ij = (alpha[t][i]*float(A[i][j])*float(B[j][seq[t+1]])*beta[t+1][j])
                gamma_i += gamma_ij
                gamma_ij_temp.append(gamma_ij)
            gamma_i_t.append(gamma_i)
            gamma_ij_t.append(gamma_ij_temp)
        gamma_i_matrix.append(gamma_i_t)
        gamma_ij_matrix.append(gamma_ij_t)
    gamma_i_matrix.append(alpha[T-1])
    return gamma_ij_matrix, gamma_i_matrix

def re_estimate(A, B, pi, gamma_ij, gamma_i, seq):
    N = len(A)
    T = len(alpha)
    # re-estimate π
    for i in range(N):
        pi[0][i] = gamma_i[0][i]

    #re-estimate A
    for i in range(N):
        denom = 0
        for t in range(T-1):
            denom += gamma_i[t][i]
        for j in range(N):
            numer = 0
            for t in range(T-1):
                numer += gamma_ij[t][i][j]
            A[i][j] = numer/denom

    #re-estimate B
    for i in range(N):
        denom = 0
        for t in range(T):
            denom += gamma_i[t][i]
        for j in range(len(B[0])):
            numer = 0
            for t in range(T):
                if (seq[t] == j):
                    numer += gamma_i[t][i]
            B[i][j] = numer/denom

    return pi, A, B
    

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
iters = 0
maxIters = 1000
oldLogProb = float("-inf")
# compute alpha-pass
while iters < maxIters:
    logProb = 0

    alpha, c_T = alpha_p(pi, A, B, seq)
    beta = beta_p(A, B, seq[::-1], c_T[::-1])
    gamma_ij, gamma_i = gamma(A, B, alpha, beta, seq)
    pi, A, B = re_estimate(A, B, pi, gamma_ij, gamma_i, seq)
    for i in range(len(seq)):
        logProb += math.log((c_T[i]))
    logProb = -logProb
    if logProb <= oldLogProb:
        break
    oldLogProb = logProb
    iters += 1 

transitionMatrix = ""
for row in range(N):
    for col in range(N):
        transitionMatrix += str(round(A[row][col],6)) + " "
print(N, N, transitionMatrix)

emissionMatrix = ""
for row in range(N):
    for col in range(len(B[0])):
        emissionMatrix += str(round(B[row][col],6)) + " "
print(N, len(B[0]), emissionMatrix)




