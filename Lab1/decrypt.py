#!/usr/bin/env python2

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
import sys,os,signal
import binascii

def alarm(time):
    def handler(signum, frame):
        print 'Timeout. Bye~'
        exit()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(time)

# Get public key
def getpubkey():
    with open('./pub.pem','rb') as f:
        pub = f.read()
        key = RSA.importKey(pub)

    return key

# Check if u send me the flag !
def check(cipher_text,pubkey):
    with open('./flag','r') as f:
        flag = f.read().strip()

        # Use binascii.hexlify to transfer byte string into integer
        # then use RSA to encrypt it
        # usage ref https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA._RSAobj-class.html#encrypt
        flag_enc = pubkey.encrypt(int(binascii.hexlify(flag),16),'')[0]


        d = SHA256.new()
        dd = SHA256.new()

        # use binascii.unhexlify to transfer integer into byte string
        d.update(binascii.unhexlify(hex(flag_enc)[2:-1]))


        try :
            dd.update(base64.b64decode(cipher_text))
        except TypeError:
            print 'base64 decode error!'
            sys.exit()

        if d.hexdigest() == dd.hexdigest():
            return 0
        return 1

# decrypt the cipher_text you send
def decrypt(cipher_text):
    with open('./priv.pem','rb') as f:
        priv = f.read()
        key = RSA.importKey(priv)
        try :
            text = key.decrypt(base64.b64decode(cipher_text))
        except TypeError:
            print 'base64 decode error!'
            sys.exit()

        print 'Decrypted message in base64 encoding format: '
        print base64.b64encode(text)

def chosen_ciphertext_attack(rsa_n, rsa_e, ciphertext, pubkey):
    """
    RSA chosen_ciphertext_attack
    choose X where X is relatively prime to n
    create Y = C*X^e mod n
    get Z = decrypted Y
    Z = Y d = (C*X^e ) d = C^d *X^ed = C^d *X = P^ed *X = P*X mod n
    find out X -1 , the modular inverse of X
    P = Z*X -1 mod n


    method 1: use rsa_n - 1 vs rsa_n which they are co_prime, which is too hard
    method 2: use 2 vs rsa_n since rsa_n is a big prime number, s.t. it must be an odd number so choose 2 to be X
    since the n is an od number, we first try the prime 2 which must be a co_prime with n, so we take 2 as X
    then the chosen_ciphertext Y will be (2^e)*(flag.enc) mod n
    use the online decrypter from TA to fetch Z


    base64 --> hex --> int   ATTACK GET C --> hex -->base64 get Z
    Z with modulo inverse get P
    """
    ciphertext = base64.b64decode(ciphertext) #decode the base64-encoded ciphertext using the base64.b64decode library
    print("ciphertext after b64decode is ",ciphertext)
    ciphertext = binascii.hexlify(ciphertext) #convert the base64 encoded value to hex
    ciphertext = long(ciphertext, 16) #convert hex to long (large long) with 16 option which is hex
    forged_number = 2 #choose X where X is relatively prime to n
    print("ciphertext is ",ciphertext)
    print("Public key n part",rsa_n)
    print("Public key e part",rsa_e)
    chosen_ciphertext = ( long(ciphertext) * (forged_number ** (long(rsa_e))) ) % (rsa_n) #create Y = C*X^e mod n
    print("chosen_ciphertext in L is ",chosen_ciphertext) #now we have Y, Let's send to server for Z = decrypted Y
    chosen_ciphertext = hex(chosen_ciphertext)
    print("chosen_ciphertext in HEX is ",chosen_ciphertext) #now we have Y, Let's send to server for Z = decrypted Y
    chosen_ciphertext = binascii.unhexlify(str(chosen_ciphertext))
    print("chosen_ciphertext in UNHEX is ",chosen_ciphertext) #now we have Y, Let's send to server for Z = decrypted Y
    chosen_ciphertext = base64.b64encode(str(chosen_ciphertext))#encode into base 64 again, argument should be string
    print("chosen_ciphertext in base64 is ",chosen_ciphertext) #now we have Y, Let's send to server for Z = decrypted Y
    return chosen_ciphertext

def base64_test():
    base64_test_str = raw_input("Enter a base64 string ")
    base64_test_str = base64.b64decode(base64_test_str)
    base64_test_str = binascii.hexlify(base64_test_str) #convert the base64 encoded value to hex
    base64_test_str = long(base64_test_str,16) #convert hex to long (large long) with 16 option which is hex
    print("The decoded information is ",base64_test_str)

if __name__ == '__main__' :
    alarm(60)
    sys.stdout=os.fdopen(sys.stdout.fileno(),"wb",0)
    key = getpubkey()

    cipher_text = raw_input('Give me your encrypted message in base64 encoding format : ').strip()
    chosen_ciphertext_attack(key.n, key.e, cipher_text, key)
    base64_test()
    if check(cipher_text,key) :
        decrypt(cipher_text)
    else :
        print 'You wish!'
