import numpy as np
import sys
import logging
from cipher.cipher import Cipher
from cipher.mathutils import random_poly
from sympy.abc import x
from sympy import ZZ, Poly
import math

priv_key_file = "private_key"
pub_key_file = "public_key"
input_file = "flag.txt"
#log = logging.getLogger("cipher")

#n = 167
#p = 3
#q = 128

def encrypt_command(data):
    input_arr = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')
    output = encrypt(pub_key_file, input_arr, bin_output=True)
    output = np.packbits(np.array(output).astype(np.int)).tobytes().hex()
    return output


def decrypt_command(data):
    input_arr = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')
    output = decrypt(priv_key_file, input_arr, bin_input=True)
    output = np.packbits(np.array(output).astype(np.int)).tobytes().hex()
    output = bytes.fromhex(output)
    return output


def encrypt(pub_key_file, input_arr, bin_output=False):
    pub_key = np.load(pub_key_file, allow_pickle=True)
    cipher = Cipher(int(pub_key['N']), int(pub_key['p']), int(pub_key['q']))
    cipher.h_poly = Poly(pub_key['h'].astype(np.int)[::-1], x).set_domain(ZZ)
    if cipher.N < len(input_arr):
        raise Exception("Input is too large for current N")
    output = (cipher.encrypt(Poly(input_arr[::-1], x).set_domain(ZZ),
                            random_poly(cipher.N, int(math.sqrt(cipher.q)))).all_coeffs()[::-1])
    if bin_output:
        k = int(math.log2(cipher.q))
        output = [[0 if c == '0' else 1 for c in np.binary_repr(n, width=k)] for n in output]
    return np.array(output).flatten()

def decrypt(priv_key_file, input_arr, bin_input=False):
    priv_key = np.load(priv_key_file, allow_pickle=True)
    cipher = Cipher(int(priv_key['N']), int(priv_key['p']), int(priv_key['q']))
    cipher.f_poly = Poly(priv_key['f'].astype(np.int)[::-1], x).set_domain(ZZ)
    cipher.f_p_poly = Poly(priv_key['f_p'].astype(np.int)[::-1], x).set_domain(ZZ)
    if bin_input:
        k = int(math.log2(cipher.q))
        pad = k - len(input_arr) % k
        if pad == k:
            pad = 0
        input_arr = np.array([int("".join(n.astype(str)), 2) for n in
                              np.pad(np.array(input_arr), (0, pad), 'constant').reshape((-1, k))])
    if cipher.N < len(input_arr):
        raise Exception("Input is too large for current N")
    return cipher.decrypt(Poly(input_arr[::-1], x).set_domain(ZZ)).all_coeffs()[::-1]


def main():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    #ch.setLevel(logging.DEBUG)
    #ch.setLevel(logging.INFO)
    ch.setLevel(logging.WARN)
    root.addHandler(ch)

    #poly_input = False
    #poly_output = False
    input_arr, output = None, None
    
    print("**********      B E Y O N D   Q U A N T U M      **********\n")
    print("   I heard that quantums are flying around these days and")
    print("people are thinking of attacking cryptosystems with them.")
    print("So I found this awesome cryptosystem that is safe from")
    print("quantums! You can send as many qubits as you like at this")
    print("cipher, and none of them will quantum break it (although")
    print("that was a fun game). Here is a proof of concept to show")
    print("the world how robust our cryptosystem is. \n")

    print("   Send us a command and its encrypted version, and we")
    print("will reply with words of praise.\n")

    while True:
        print("Usage: ")
        print("   encrypt <command>")
        print("   execute <ciphertext> <command>")
        sys.stdout.flush()
        parts = sys.stdin.readline()[:-1].split(" ")

        try:
            if parts[0] == "encrypt":
                spell = parts[1]
                print(encrypt_command(bytes.fromhex(spell)))
                sys.stdout.flush()
            elif parts[0] == "execute":
                ct = bytes.fromhex(parts[1])
                command = bytes.fromhex(parts[2])
                if command not in decrypt_command(ct):
                    raise Exception()
                if command == b"cat flag.txt":
                    print("encrypted command: " + encrypt_command(command))
                    print("ciphertext: " + str(parts[1]))
                    if encrypt_command(command) == parts[1]: # ct
                        print("Hey, you tried to run a forbidden command.")
                        sys.stdout.flush()
                        raise Exception()
                    else:
                        print("What?! How did you do that??")
                        with open("flag.txt") as file:
                            print("".join(file.readlines()))
                else:
                    print("Your command was valid! We executed it and you are awesome :)\n")
                sys.stdout.flush()
            elif parts[0] in ["quit", "exit"]:
                print("Bye!")
                sys.stdout.flush()
                return
            else:
                raise Exception()
        except:
            print("Something went wrong...")
            print("...try again?\n")
            sys.stdout.flush()
    
if __name__ == "__main__":
    main()
