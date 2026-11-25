
import secrets
import hashlib
import random
import os


# To make transaction you need 3
# Flow should go like
# 1 . Address  - Make address or identity
	# 1.1 obtain seed funds
# 2 . Enter x amount
# 3 . Set network fee

# prime field
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
# Number of points we can hit in the curve 
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# Generator points
g = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
a = 0
O = None

privKey = []
# Generates private key - Random 256 bit number
# 1 < K < n
# min: 1
# max: 115792089237316195423570985008687907852837564279074904382605163141518161494336
def PrivKeyGen():
    # Generates 256 bits

    file_path = "privkey.txt"
    if os.path.isfile(file_path):
        with open("privkey.txt", "r", encoding="utf-8") as file:
            content = file.read()
            print(content)

    else:
        key = secrets.randbelow(n - 1) + 1  # 1 <= key <= n-1
        with open("privkey.txt", "w", encoding="utf-8") as file:
            file.write(str(key))
        privKey.append(key)


def publicKeyGen():
    with open("privkey.txt", "r", encoding="utf-8") as file:
        private_key = int(file.read().strip())
    public_key = multiply(private_key, g, a, p)
    return public_key

# a is number, m is modulus
def mod_inverse(a: int, m: int) -> int:
    r0, r1 = a, m
    s0, s1 = 1, 0

    while r1 != 0:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        s0, s1 = s1, s0 - quotient * s1

    if r0 != 1:
        raise ValueError(f"{a} has no modular inverse modulo {m}")

    return s0 % m


# point, a, p ?
def double(point, a, p):
    if point is O:
        return O

    x1, y1 = point

    if y1 == 0:
        return O

    # slope = (3x1^2 + a) / (2y1)
    numerator = (3 * x1**2 + a) % p
    denominator = (2 * y1) % p

    slope = (numerator * mod_inverse(denominator, p)) % p

    x3 = (slope**2 - 2 * x1) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return x3, y3

# P, Q, a, p ?
def add(P, Q, a, p):
    if P is O:
        return Q
    if Q is O:
        return P

    x1, y1 = P
    x2, y2 = Q

    if P == Q:
        return double(P, a, p)

    if x1 == x2:
        return O

    # slope = (y2 - y1) / (x2 - x1)
    numerator = (y2 - y1) % p
    denominator = (x2 - x1) % p

    slope = (numerator * mod_inverse(denominator, p)) % p

    x3 = (slope**2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return x3, y3

# K, point (X,Y), a, p?
def multiply(k, point, a, p):
    result = O
    current = point

    while k > 0:
        if k & 1:
            result = add(result, current, a, p)

        current = double(current, a, p)
        k >>= 1

    return result

PrivKeyGen()
public_key = publicKeyGen()

with open("privkey.txt", "r", encoding="utf-8") as file:
    private_key = int(file.read().strip())

print("Public Key X:", public_key[0])
print("Public Key Y:", public_key[1])

# TODO 1. Verfication that public key is on    the curve
# TODO 2 . Bitcoin P2PKH
# TODO verification that public key is on the curve
# TODO We are going to create, digitally sign, and broadcast a Bitcoin transaction in pure Python
