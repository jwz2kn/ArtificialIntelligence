__author__ = 'John Zhang', 'Tyler Ealy'

# Initializations of global variables
U = {}
U_prime = {}
R = {}
S = list()

MAX_ITERS = 1000
iters = 0
d = 0
sigma = 0.001
gamma = 1
windCase = 1

gridMin = 0
gridMax = 6

def initialize():
    for i in range(7):
        for j in range(7):
            S.append((i,j))
            U_prime[i, j] = 0.0
            R[i, j] = -1.0
            if i == 3 and j == 6:
                R[i, j] = 0.0

def U_prime_toString():
    U_primeStr = ""
    for i in range(7):
        for j in range(7):
            U_primeStr = U_primeStr + str('%.1f' % U_prime[(i,j)]) +" " +"\t"
        U_primeStr += "\n"
    return U_primeStr

def U_toString():
    U_Str = ""
    for i in range(7):
        for j in range(7):
            U_Str = U_Str + str('%.1f' % U[(i,j)]) +" " +"\t"
        U_Str += "\n"
    return U_Str

def actionResultList((i,j)):
    U_prime_sprime = list()
    Actions = list()
    Stay = [i,j]
    N = [i-1, j]
    NE = [i-1, j+1]
    E = [i, j + 1]
    SE = [i + 1, j + 1]
    S = [i + 1, j]
    SW = [i + 1, j - 1]
    W = [i, j - 1]
    NW = [i - 1, j - 1]

    Actions.append(Stay);
    Actions.append(N); Actions.append(NE); Actions.append(E); Actions.append(SE);
    Actions.append(S); Actions.append(SW); Actions.append(W); Actions.append(NW);

    for a in Actions:
        if windCase != 1 and (a[1] == 3+1 or a[1] == 4+1 or a[1] == 5+1):
            a[0] = a[0] - windCase + 1
        if a[0] > 6:
            a[0] = 6
        if a[0] < 0:
            a[0] = 0
        if a[1] > 6:
            a[1] = 6
        if a[1] < 0:
            a[1] = 0
        U_prime_sprime.append([tuple(a), U_prime[tuple(a)]])

    return U_prime_sprime

def maximizer(l):
    maximum = -10000000
    length = len(l)
    for i in range(length):
        if U[l[i][0]]*l[i][1] > maximum:
            maximum = U[l[i][0]]*l[i][1]
    return maximum

def main():
    global iters, U, U_prime, d, windCase
    initialize()
    print "Value Iterator."
    windCase = int(raw_input("Please type wind case 1, 2, or 3.\n"))
    print "Initial U\'"
    print U_prime_toString()
    while True:
        U = U_prime
        d = 0
        for s in S:
            U_prime[s] = R[s] + maximizer(actionResultList(s))
            if abs(U_prime[s] - U[s]) > d:
                d = abs(U_prime[s] - U[s])
        print "Iteration", iters
        print U_prime_toString()
        iters += 1
        if (d < sigma) or (iters > MAX_ITERS):
            break
    # # do something with U prime
    print "U\' after Value Iteration in Case", windCase
    print U_prime_toString()

    return

if __name__ == "__main__":
    main()