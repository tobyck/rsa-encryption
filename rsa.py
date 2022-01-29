import random, time

# Toby Connor-Kebbell
# January 2022
# Pure python implementation of RSA encryption

# greatest common divisor (euclidean algorithm)
def gcd(x, y):
    while x != y:
        if x > y:
            x -= y
        else:
            y -= x
    return x

# primality test
# n is the number to test
# k in the number of rounds
# s is the exponent
def rabin_miller(n, k):
    s = n - 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x in [1, -1]:
            continue
        else:
            return False
    return True

# generate random prime
def grp(bits):
    while True:
        x = random.randrange(2 ** (bits - 1) + 1, 2 ** bits - 1, 2)
        if pow(2, x - 1, x) == 1:
            if rabin_miller(x, 40):
                return x

# extended euclidean algorithm
# returns bezouts coefficients a and b
# r is the remainder
# q is the quotient
def bezout(x, y, a = 0, b = 1, pa = -1, pb = 0):
    if y > x:
        x, y = y, x
    r = x % y
    if r == 0:
        return a, b
    else:
        q = x // y
        a, b, pa, pb = q * a + pa, q * b + pb, a, b
        print(x, y, q, r, a, b, pa, pb)
        return bezout(y, r, a, b, pa, pb)


# p and q = prime numbers (1024 bits is reccomended)
# n = p * q
# phi = (p - 1) * (q - 1)
# choose e such that gcd(e, phi) = 1
# choose d such that (e * d) mod phi = 1
# i and j are e and d candidates
def gkp(bits):
    start = time.time()
    p, q = grp(bits), grp(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = bezout(e, phi)[0]
    if d < 0:
        d += phi
    
    key_data = {
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "public": e,
        "private": d,
        "modulus": n,
        "time": time.time() - start
    }

    return key_data

# interface
# m is the message
# c is the cipher
# c = m ^ e mod n
# m = c ^ d mod n
keyring = {}
chars = [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}\|;'\":,./<>?`~ "]
bits = int(input("\nEnter the number of bits for p and q: "))
print("\nGenerating key pair...\n")
key_data = gkp(bits)
print("Public key: "+str(key_data["public"])+"\n\nPrivate key: "+str(key_data["private"])+"\n\nModulus: "+str(key_data["modulus"])+"\n\nKey pair generated in "+str(round(key_data["time"], 2))+" seconds")
while True:
    print("\n1. Generate new key pair\n2. Add key to keyring\n3. Set encryption key\n4. Encrypt\n5. Decrypt\n6. Exit")
    choice = input("\nSelect action: ")
    if choice == "1":
        bits = int(input("Enter the number of bits for p and q: "))
        print("Generating key pair...\n")
        print("Public key: "+str(key_data["public"])+"\n\nPrivate key: "+str(key_data["private"])+"\n\nModulus: "+str(key_data["modulus"])+"\n\nKey pair generated in "+str(round(key_data["time"], 2))+" seconds")
        key_data = gkp(bits)
    elif choice == "2":
        name = input("\nName: ")
        keyring[name] = (int(input("Key (without modulus): ")), int(input("Modulus: ")))
    elif choice == "3":
        if len(keyring) == 0:
            print("\nNo keys in keyring")
            time.sleep(1.2)
        else:
            for i in keyring:
                print("\n"+i+": "+str(keyring[i]))
            name = input(f"\nSelect encryption key (e.g. {random.choice(list(keyring))}): ")
            encrypt_key = keyring[name][0]
            encrypt_mod = keyring[name][1]
            print("\nEncryption key set to "+str(encrypt_key)+", "+str(encrypt_mod)+" ("+name+"'s key)")
    elif choice == "4":
        m = input("\nMessage: ")
        c = [str(pow(chars.index(k), encrypt_key, encrypt_mod)) for k in m]
        print("Cipher:", " ".join(c))
    elif choice == "5":
        c = [int(l) for l in input("\nCipher: ").split(" ")]
        m = [chars[pow(k, key_data["private"], key_data["modulus"])%len(chars)] for k in c]
        print("Message:", "".join(m))
    elif choice == "6":
        exit()
    else:
        print("\ninvalid input")    
