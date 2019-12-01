import random
import sys


################################################################################################################

# Returns gcd of x and y
def gcd(x,y):
    if x<y:
        (x, y) = (y, x)

    while y>0:
        (x, y) = (y, x%y)

    return x

################################################################################################################

# Extended Euclidean algo (if xa+yb = gcd(x,y), returns x,y,gcd(x,y))
def extEuclid(x, y):
    t, u = 1, 0
    v, w = 0, 1

    while y>0:
        q = x // y
        (t, u) = (u, t - q*u)
        (v, w) = (w, v - q*w)
        (x, y) = (y, x - q*y)

    return (t, v, x)

################################################################################################################

# Returns d such that de = 1 (mod n)
def modInv(n, e):

    return (extEuclid(e,n)[0])%n

################################################################################################################

# Returns integer square root
def intSqrt(n):
    
    if n == 0 or n == 1:
        return n

    u = n.bit_length()//2
    v = n.bit_length()%2

    x = 2**(u+v)

    while True:
        
        y = (x + n//x)//2
        if y >= x:
            break
        else:
            x = y

    if (x*x) == n:
        return x

    return -1

################################################################################################################

# One pass of the miller Rabin test
def MillerRabinOneTest(a, u, r, p):

	ar = pow(a, r, p)
	
	# Test 1
	if ar == 1:
		return True
	
	# Loop for Test 2 
	for _ in range(u):
		if (ar == p - 1):
			return True
		ar = (ar * ar) % p
	
	# Final condition
	return (ar==p - 1)

################################################################################################################

# Function to perform Miller-Rabin test for num_tests random bases
def MillerRabinTestComplete(p):
	 
	#p-1 = (2^u)r, with odd r
	r = p-1
	u = 0
	while (r%2 == 0):
		r = r//2
		u+=1
	
	num_tests = 20
	
	for _ in range(num_tests):

		a = random.randrange(2,p-1)
		if not MillerRabinOneTest(a, u, r, p):
			return False
	return True

################################################################################################################

# Prime number generator using Miller-Rabin test
def getPrime(nbits):
	while True:
		p = random.getrandbits(nbits)

		# Make the length of p as nbits
		p = p | (2**nbits)
		#Make p odd
		p |= 1

		if MillerRabinTestComplete(p):
			return p
        
################################################################################################################

# Generates a prime number q within the given range
def getPrimeIn(start, stop):
	while True:
		q = random.randrange(start,stop-1)

		# Making q odd
		q = q | 1

		#Check for primality
		if MillerRabinTestComplete(q):
			return q

################################################################################################################

# Get p and q
def getPQ(nbits=512):
    
    p = getPrime(nbits)
    q = getPrimeIn(p+1, 2*p)
    
    return (p,q)

################################################################################################################

# Generate public and private keys vulnerable to Wiener's attack
def getKeys(nbits=1024):
    
    (p,q) = getPQ(nbits//2)

    N = p*q
    totient = (p-1) * (q-1)
        
    isGood_d = False

    # Loop to generate private decryption exponent
    while not isGood_d:
        d = random.getrandbits(nbits//4)
        if gcd(d,totient) == 1 and 36*pow(d,4) < N :
            isGood_d = True
                    
    e = modInv(totient, d)
    
    return (N, e, d)

################################################################################################################