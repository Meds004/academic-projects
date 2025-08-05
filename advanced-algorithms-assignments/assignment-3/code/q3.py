# Advanced Algorithms Assignment 3 Question 3
# Anthony Medico

# This script is used to crack a Rabin cipher (Y).

import math

### Global variables ###
n = 496829 # public key
Y = [3874, 98671, 239225, 461557, 437975, 426701, 3874, 310672,
     396855, 313859, 167894, 63899, 220458, 35143, 200298, 237462,
     492881, 254473, 218099, 64830, 172978, 461557, 395471, 415614,
     308094, 475083, 19084, 27808, 42610, 110617, 403533, 102393] # cipher text

solutions = [[], [], [], []] # to store results

### Function definitions ###

# check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    for i in range(3, num // 2):
        if num % i == 0:
            return False

    return True

# Square and multiply from slides, slightly adapted
# c is a string of the binary representation (a bit easier to work with here)
def square_and_multiply(y, c, n):
    z = 1
    for bit in c:
        z = (z * z) % n
        if bit == '1':
            z = (z * y) % n

    return z

# Chinese Remainder Theorem, from slides
def crt(a1, a2, m1, m2):
    M = m1 * m2
    M1 = M // m1
    M2 = M // m2

    y1 = multiplicative_inverse(m1, M1)
    y2 = multiplicative_inverse(m2, M2)

    return (a1 * m2 * y1 + a2 * m1 * y2) % M

# Multiplicative inverse algorithm, from slides
def multiplicative_inverse(phi, b):
    phi0 = phi
    b0 = b
    t0 = 0
    t = 1
    q = phi0 // b0
    r = phi0 - q * b0

    while r > 0:
        temp = (t0 - q * t) % phi
        t0 = t
        t = temp
        phi0 = b0
        b0 = r
        q = phi0 // b0
        r = phi0 - q * b0

    if b0 != 1:
        return -1
    else:
        return t

# Converts x back to a string
def x_to_string(x):
    letters = ''
    for i in [3, 2, 1, 0]: # exponents for 26
        quotient = x // (26 ** i)
        remainder = x % (26 ** i)
        x = remainder # continue with remainder
        letters += (chr(quotient + ord('a'))) # calculate ascii value and convert to char
    return letters


### Program start ###
# Brute force factor n to find p and q
p = 0
q = 0
for i in range(3, math.isqrt(496829)): # using integer square root function
    if is_prime(i):
        if n % i == 0:
            if is_prime(n // i):
                p = i
                q = n // i

# From the above code: p=691, q=719
print(f"p = {p}, q = {q}\n")

# Solve each Y
for y in Y:
    # calculate congruences
    c1 = (p + 1) // 4 # calculate the exponent
    c1 = bin(c1)[2:] # convert to string of binary representation
    n1 = p
    x_c1 = square_and_multiply(y, c1, n1) # first congruence

    c2 = (q + 1) // 4
    c2 = bin(c2)[2:]
    n2 = q
    x_c2 = square_and_multiply(y, c2, n2) # second congruence

    print(f"The congruences for y = {y} are x ≡ ±{x_c1} (mod {p}) and x ≡ ±{x_c2} (mod {q})")

    # use Chinese Remainder Theorem for all cases
    x_1 = crt(x_c1, x_c2, p, q)
    x_2 = crt(x_c1*-1, x_c2, p, q)
    x_3 = crt(x_c1, x_c2*-1, p, q)
    x_4 = crt(x_c1*-1, x_c2*-1, p, q)

    # change x back to a string, record all solutions
    solutions[0].append(x_to_string(x_1))
    solutions[1].append(x_to_string(x_2))
    solutions[2].append(x_to_string(x_3))
    solutions[3].append(x_to_string(x_4))

# print all plaintext possibilities to select manually

# Commented out code below prints it on two lines instead of one
# print()
# for i in range(len(solutions)):
#     for j in range(len(solutions[i]) // 2):
#         print(solutions[i][j], end=" ")
#     print()
#
# print()
# for i in range(len(solutions)):
#     for j in range(len(solutions[i]) // 2, len(solutions[i])):
#         print(solutions[i][j], end=" ")
#     print()

# All printed on one line
print()
for i in range(len(solutions)):
    for j in range(len(solutions[i])):
        print(solutions[i][j], end=' ')
    print()