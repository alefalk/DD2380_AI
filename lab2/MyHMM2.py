import sys

# pypy3 MyHMM2.py < test.in

def vectorMul(A, B, colnum):
    alpha = []
    maxindex=0
    value = 0
    for i in range(len(A)):
        val = float(A[i]) * float(B[i][colnum])
        alpha.append(val)
        if val > value:
            value = val
            maxindex = i
   # print("at index: ", maxindex, "val is: ",value)
   # print(alpha)

    return [alpha], maxindex

def vectorMulViterbi(delta, A, B, colnum):
    
    max_prob_vector = []
    maxindex = 0
    value = 0

    for i in range(len(delta)):
        prob_vector = []
        for j in range(len(A)):
            val = float(delta[j]) * float(A[j][i]) * float(B[i][colnum])
           # print("row:", i, "delta: ", float(delta[j]), "A[i][j]:", float(A[j][i]), "B[j][col]: ", float(B[i][colnum]), "mult: ",val )

            prob_vector.append(val)
        max_prob_vector.append(max(prob_vector))
        
        if max(prob_vector) > value :
            value = max(prob_vector)
            maxindex = i
  #  print("at index: ", maxindex, "val is: ",value)
   # print(max_prob_vector)
    return [max_prob_vector], maxindex  

def viterbi(seq, A, B, delta):
    #print(seq)
    if len(seq) == 0 :
        return most_likely
    max_prob_vector, maxindex = vectorMulViterbi(delta[0], A, B, seq[0])
    #print(max_prob_vector)
    most_likely.append(maxindex)
    return viterbi(seq[1:], A , B, max_prob_vector)

most_likely=[]
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
delta_init, maxindex = vectorMul(pi[0], B, seq[0])
most_likely.append(maxindex)
h = viterbi(seq[1:], A, B, delta_init)
print(' '.join(map(str, h)))
