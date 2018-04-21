import base64
import binascii
import os
import sys

with open('decoded_memo.txt', 'r') as fptr:
    # print fptr.read()
    all_data = str(fptr.read())
    # print(all_data)
    print(type(all_data))

    xor_key = sys.argv[1]

    key_len = len(xor_key)
    total_len = len(all_data)
    decrypted_data = "" #the xor-decrypted data will be here

    print('key', xor_key, 'Keylen', key_len, 'total data len', total_len)
    for i in range(0, total_len, key_len):
        for j in range (0, key_len, 1):
            #print('i ', i, ' and j ', j , '\n')
            decrypted_data += chr(ord(all_data[i + j]) ^ ord(xor_key[j])) #ord for char->int and chr vice versa

    with open('xorkey_decrypted_data.txt', 'w') as fptr2:
        fptr2.write(decrypted_data)
