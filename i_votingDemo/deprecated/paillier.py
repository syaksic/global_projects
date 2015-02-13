import math
import primes

def invmod(a, p):
    '''
    http://code.activestate.com/recipes/576737-inverse-modulo-p/
    The multiplicitive inverse of a in the integers modulo p.
    Return b s.t.
    a * b == 1 mod p
    '''
    r = a
    d = 1
    while True:
        d = ((p // r + 1) * d) % p
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

class PrivateKey(object):
    def __init__(self, bits):
        p = primes.generate_prime(bits / 2)
        q = primes.generate_prime(bits / 2)
        n = p * q
        self.lam = (p-1) * (q-1)
        self.pub = PublicKey(bits, n)
        self.mu = invmod(self.lam, n)

class PublicKey(object):
    def __init__(self, bits, n):
        self.bits = bits
        self.n = n
        self.n_sq = n * n
        self.g = n + 1

def encrypt(plain, pub):
    while True:
        r = primes.generate_prime(long(round(math.log(pub.n, 2))))
        if r > 0 and r < pub.n:
            break
    x = pow(r, pub.n, pub.n_sq)
    cipher = (pow(pub.g, plain, pub.n_sq) * x) % pub.n_sq
    return cipher

def e_add(pub, a, b):
    return a * b % pub.n_sq

def decrypt(cipher, priv):
    pub = priv.pub
    x = pow(cipher, priv.lam, pub.n_sq) - 1
    plain = ((x // pub.n) * priv.mu) % pub.n
    return plain
