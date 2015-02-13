from paillier import *

print "Generating keypair..."
priv = PrivateKey(128)
pub = priv.pub

x = 3
print "x =", x
print "Encrypting x..."
ex = encrypt(x, pub)
print "ex =", ex

y = 5
print "y =", y
print "Encrypting y..."
ey = encrypt(y, pub)
print "ey =", ey

print "Computing ex + ey..."
er = e_add(pub, ex, ey)
print "er =", er

print "Decrypting er..."
r = decrypt(er, priv)
print "r =", r
