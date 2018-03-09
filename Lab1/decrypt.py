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

def chosen_ciphertext_attack(rsa_n, rsa_e, ciphertext):
    """
    method 1: use rsa_n - 1 vs rsa_n which they are co_prime
    method 2: use 2 vs rsa_n since rsa_n is a big prime number, s.t. it must be an odd number so choose 2 to be X
    will probably fit the case
    """
    ciphertext = base64.b64decode(ciphertext)
    ciphertext = binascii.hexlify(ciphertext) #convert the base64 encoded value to hex
    ciphertext = long(ciphertext,16) #convert hex to long (large long) with 16 option which is hex
    print("ciphertext is ",ciphertext)
    print("Public key n part",rsa_n)
    print("Public key e part",rsa_e)
    chosen_ciphertext = (2 ** (long(rsa_e))) * long(ciphertext) % (rsa_n)
    print("chosen_ciphertext in L is ",chosen_ciphertext) #now we have Y, Let's send to server for Z = decrypted Y
    chosen_ciphertext = base64.b64encode(str(chosen_ciphertext))#encode into base 64 again, argument should be string
    print("chosen_ciphertext in base64 is ",chosen_ciphertext) #now we have Y, Let's send to server for Z = decrypted Y
    return chosen_ciphertext


if __name__ == '__main__' :
    alarm(60)
    sys.stdout=os.fdopen(sys.stdout.fileno(),"wb",0)
    key = getpubkey()

    cipher_text = raw_input('Give me your encrypted message in base64 encoding format : ').strip()

    chosen_ciphertext_attack(key.n, key.e, cipher_text)

    if check(cipher_text,key) :
        decrypt(cipher_text)
    else :
        print 'You wish!'
