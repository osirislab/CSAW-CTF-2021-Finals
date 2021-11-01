#from gmpy2 import divm, mpz, mul, powmod
from pwn import remote, process
import sys
import time
import binascii

host = "localhost" #"crypto.chal.csaw.io"
port = 5000 # 5009

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


def encrypt_message(msg):
	server.send(" ".join(["encrypt", msg.hex()]) + "\n")
	ct = server.recvuntil("\n").strip()
	server.recvuntil("exit\n")
	return ct

def execute(ct, msg):
	server.send(b" ".join([b"execute", ct, binascii.hexlify(msg)])+b"\n")
	server.recvuntil("exit\n")

# Adds exactly one to what presumably is a low-order byte of some ciphertext (i.e. in the padding somewhere)
def increment_ct_byte(ct, offset_from_end):
	print("ct = " + str(ct))
	ct_bytes = binascii.unhexlify(ct)
	ct_bytes_list = list(ct_bytes)
	print("ct_bytes_list = " + str(ct_bytes_list))
	ct_bytes_list[len(ct_bytes_list)-offset_from_end]=ct_bytes_list[len(ct_bytes_list)-offset_from_end]+1 #1
	new_ct = binascii.hexlify(bytes(ct_bytes_list))
	return new_ct

def main():

	server.interactive()
	# Test to decrypt a message twice and make sure the ciphertext is completely different each time
	server.recvuntil("exit\n")
	msg = b"This is a test"
	ct = encrypt_message(msg)
	print("ct = " + str(ct))
	#msg = b"This is a test"
	#server.send(" ".join(["encrypt", msg.hex()]) + "\n")
	#server.interactive()
	#ct = server.recvuntil("\n").strip()
	#server.send(b" ".join([b"execute", ct, binascii.hexlify(msg)])+b"\n")
	#execute(ct, msg)
	#server.recvuntil("exit\n")

	#execute(ct, msg)
	#server.recvuntil("exit\n")

	#execute(ct, msg)
	#server.recvuntil("exit\n")

	new_ct = increment_ct_byte(ct=ct, offset_from_end=2)
	print("Old ct = " + str(ct))
	print("New ct = " + str(new_ct))
	execute(new_ct, msg)
	server.interactive()

	msg = b"This is a test"
	server.send(" ".join(["encrypt", msg.hex()]) + "\n")
	#server.interactive()
	ct = server.recvuntil("\n").strip()
	server.send(b" ".join([b"execute", ct, binascii.hexlify(msg)])+b"\n")
	server.recvuntil("exit\n")
	server.interactive()

	'''
	#server.recvuntil("execute <ciphertext> <command>\n")
	server.recvuntil("exit\n")
	#server.send("encrypt 61616161")
	#msg = b"test message"
	msg = b"cat flag.txt"
	server.send(" ".join(["encrypt", msg.hex()]) + "\n")
	#server.interactive()
	flag_ct = server.recvuntil("\n").strip()
	#server.interactive()
	#print("flag_ct = " + str(flag_ct))
	flag_ct_bytes = binascii.unhexlify(flag_ct)
	flag_ct_bytes_list = list(flag_ct_bytes)
	#print("flag_ct_bytes_list = " + str(flag_ct_bytes_list))

	server.recvuntil("exit\n")
	msg2 = b"cat flag.txta"
	server.send(" ".join(["encrypt", msg2.hex()]) + "\n")
	#server.interactive()
	wrong_ct = server.recvuntil("\n").strip()
	#server.interactive()
	#print("wrong ciphertext = " + str(wrong_ct))
	wrong_ct_bytes = binascii.unhexlify(wrong_ct)
	wrong_ct_bytes_list = list(wrong_ct_bytes)
	#print("wrong_ct_bytes_list = " + str(wrong_ct_bytes_list))
    '''

	# Test solution
	#flag_ct_bytes_list[len(flag_ct_bytes_list)-2]=flag_ct_bytes_list[len(flag_ct_bytes_list)-2]+1 #1

	#new_ct = binascii.hexlify(bytes(flag_ct_bytes_list))
	#print(b"new_ct = " + new_ct)
	#print(str(new_ct.__class__))
	#server.send(b" ".join([b"execute", new_ct, binascii.hexlify(msg)])+b"\n")


	# Test attempt to cheese the flag
	server.send(b" ".join([b"execute", wrong_ct, binascii.hexlify(msg)])+b"\n")
	server.interactive()


if __name__ == "__main__":
	main()
