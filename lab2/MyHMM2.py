import sys

def viterbi(seq, A, B, pi):
    T = len(seq)
    N = len(A)
    delta = [[0] * N for _ in range(T)]
    delta_idx = [[0] * N for _ in range(T)]

    # initalize for first state in sequence. δ1(i) = bi(o1)πi
    for i in range(N):
        delta[0][i] = float(pi[0][i]) * float(B[i][seq[0]])

    # Forward pass δt(i) = maxj∈[1,..N] a[j,i]*δt−1(j)bi(ot).
    for t in range(1, T):
        for i in range(N):
            max_value = float('-inf')
            max_j = -1
            for j in range(N):
                value = delta[t - 1][j] * float(A[j][i]) * float(B[i][seq[t]])
                if value > max_value:
                    max_value = value
                    max_j = j
            delta[t][i] = max_value
            delta_idx[t][i] = max_j
  
    # When arriving at the end of the observation sequence, T , the probability of the most likely hidden
    # state sequence is given by maxj∈[1,..N] δT
    x_T = delta[T - 1].index(max(delta[T - 1]))
    x_t = [x_T]
    # Backward pass to find the most likely path
    for t in range(T - 1, 0, -1):
        t_plus_one = x_t[0]
        x_t.insert(0, delta_idx[t][t_plus_one])
  
    return x_t

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

most_likely = viterbi(seq, A, B, pi)
print(' '.join(map(str, most_likely)))
