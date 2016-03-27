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

def initialize():
    for i in range(0, 7):
        for j in range(0, 7):
            S.append([i,j])
            U_prime[i, j] = 0.0
            R[i, j] = -1.0
            if i == 3 and j == 6:
                R[i, j] = 0.0

def main():
    global iters, U, d
    initialize()

    while d < sigma or iters > MAX_ITERS:
        U = U_prime
        d = 0
        for s in S:
            print s
            U_prime[s] = R[s] # + max action with given constraints and transition model
            if abs(U_prime[s] - U[s]) > d:
                d = abs(U_prime[s] - U[s])
        iters += 1

    # do something with U
    print U

    return

if __name__ == "__main__":
    main()