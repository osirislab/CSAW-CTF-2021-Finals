#from gmpy2 import divm, mpz, mul, powmod
from pwn import remote, process
import sys
import time
import binascii

host = "crypto.chal.csaw.io"
port = 5009

server = remote(host, port)
#server.interactive()
#server = process('python3 ./server.py', shell=True)

#key material
#n = 104525132490556452593202847360958867443850727021139374664119771884926217842051539965479047872905144890766357397753662519890618428457072902974515214064289896674717388849969373481670774897894594962128470900125169816586277785525675183392237296768481956391496477386266086799764706674035243519651786099303959008271
#e = 65537

def byte_to_int(str):
	return int(str.hex(), 16)

def hex_to_byte(hex):
	return bytes.fromhex(("0" if len(hex) % 2 else "") + hex)

def encrypt(data):
	return pow(byte_to_int(data), e, n)

def try_sign(spell):
	server.send("sign " + spell.hex() + "\n")

	line = server.recvuntil("\n").decode("utf-8")
	if line.startswith("Incorrect"):
		server.recvuntil("\n")
		return None

	#strip off \r\n
	return line[:-2].encode("utf-8")

def try_cast(spell, sig):
	server.send(" ".join(["cast", sig.hex(), spell.hex()]) + "\n")

	line = server.recvuntil("\n").decode("utf-8")
	if line.startswith("Incorrect"):
		server.recvuntil("\n")
		return False
	elif line.startswith("You"):
		return True

	#strip off \r\n
	return server.recvuntil("\n")[:-2]

class UE(BaseException):
	def __init__(self):
		pass

def main():
	server.recvuntil("execute <ciphertext> <command>\n")
	#server.send("encrypt 61616161")
	#msg = b"test message"
	msg = b"cat flag.txt"
	server.send(" ".join(["encrypt", msg.hex()]) + "\n")
	#server.interactive()
	ct = server.recvuntil("\n").strip()
	#server.interactive()
	#print("ct = " + str(ct))
	ct_bytes = binascii.unhexlify(ct)
	ct_bytes_list = list(ct_bytes)
	ct_bytes_list[len(ct_bytes_list)-2]=ct_bytes_list[len(ct_bytes_list)-2]+1
	new_ct = binascii.hexlify(bytes(ct_bytes_list))
	#print(b"new_ct = " + new_ct)
	#print(str(new_ct.__class__))
	server.send(b" ".join([b"execute", new_ct, binascii.hexlify(msg)])+b"\n")
	server.interactive()


if __name__ == "__main__":
	main()
