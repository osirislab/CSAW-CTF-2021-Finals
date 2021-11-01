import numpy as np
import sys
from cipher.cipher import Cipher
from cipher.mathutils import random_poly
from sympy.abc import x
from sympy import ZZ, Poly
import math
#import gmpy2
#from gmpy2 import mpfr, div

#priv_key_file = "private_key.npz"
#pub_key_file = "public_key.npz"
#input_file = "flag.txt"
#log = logging.getLogger("cipher")

#n = 167
#p = 3
#q = 128

def encrypt_command(data, public_key):
    #print("starting encrypt_command")
    input_arr = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    #print("input_arr = " + str(input_arr))
    input_arr = np.trim_zeros(input_arr, 'b')
    #print("input_arr = " + str(input_arr))
    #print("In encrypt_command: about to encrypt.")
    output = encrypt(public_key, input_arr, bin_output=True)
    #print("In encrypt_command: encrypted.")
    #print("output = " + str(output))
    output = np.packbits(np.array(output).astype(np.int)).tobytes().hex()
    #print("output = " + str(output))
    return output


def decrypt_command(data, private_key):
    input_arr = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')
    #print("In decrypt_command: ct = " + str(data))
    #print("   input_arr = " + str(input_arr))
    #print("   private_key = " + str(private_key))
    output = decrypt(private_key, input_arr, bin_input=True)
    #print("got output.")
    #print("output = " + str(output))
    output = np.packbits(np.array(output).astype(np.int)).tobytes().hex()
    output = bytes.fromhex(output)
    return output

def generate(N, p, q):#, priv_key_file, pub_key_file):
    #print("in generate")
    #print(str(pub_key_file))
    cipher = Cipher(N, p, q)
    #print("generated cipher")
    cipher.generate_random_keys() # creates f_poly, g_poly. Do I not need to save the g_poly?
    #print("generated random keys")
    h = np.array(cipher.h_poly.all_coeffs()[::-1])
    #print("got h")
    #print("h = " + str(h))
    #f, f_p = cipher.f_poly.all_coeffs()[::-1], cipher.f_p_poly.all_coeffs()[::-1]
    f, f_p = np.array(cipher.f_poly.all_coeffs()[::-1]), np.array(cipher.f_p_poly.all_coeffs()[::-1])
    #print("got f, f_p")
    private_key = {'N':N,'p':p,'q':q,'f':f,'f_p':f_p}
    #np.savez_compressed(priv_key_file, N=N, p=p, q=q, f=f, f_p=f_p)
    #print("saved private key to {} file".format(priv_key_file))
    #log.info("Private key saved to {} file".format(priv_key_file))
    #try:
        #print("Saving public key")
        #print("public key is {}".format(pub_key_file))
    public_key = {'N':N,'p':p,'q':q,'h':h}
    #np.savez_compressed(pub_key_file, N=N, p=p, q=q, h=h)
    #except Exception as ex:
    #    print("Something went wrong: exception was " + str(ex))
    #sleep(2)
    #print("saved public key")
    #print("saved public key to {} file".format(pub_key_file))
    #log.info("Public key saved to {} file".format(pub_key_file))
    return (private_key, public_key)

def encrypt(pub_key, input_arr, bin_output=False):
    #pub_key = np.load(pub_key_file, allow_pickle=True)
    #print("In encrypt.")
    #for key in pub_key.keys():
    #    print(str(key))
    #print("N = " + str(int(pub_key['N'])))
    #print("p = " + str(int(pub_key['p'])))
    #print("q = " + str(int(pub_key['q'])))
    #print("pub_key = " + str(pub_key))
    cipher = Cipher(int(pub_key['N']), int(pub_key['p']), int(pub_key['q']))
    #print("cipher class = " + str(cipher.__class__))
    #try:
        #print("h class = " + str(pub_key['h'].__class__))
    #    print("About to print h")
    #    print(pub_key['h'])
        #print("h = " + str(pub_key['h'].astype(np.int)))
    #except Exception as ex:
    #    print(ex)
    #print("h class = " + str(pub_key['h'].astype(np.int)))
    #print("h = " + str(pub_key['h']))
    #print("Input for Poly = " + str(pub_key['h'].astype(np.int)[::-1].__class__))
    cipher.h_poly = Poly(pub_key['h'].astype(np.int)[::-1], x).set_domain(ZZ)
    #print("cipher.h_poly = " + str(cipher.h_poly.__class__))
    if cipher.N < len(input_arr):
        raise Exception("Input is too large for current N")
    #print("About to encrypt.")
    output = (cipher.encrypt(Poly(input_arr[::-1], x).set_domain(ZZ),
                            random_poly(cipher.N, int(math.sqrt(cipher.q)))).all_coeffs()[::-1])
    #print("Encrypted.")
    if bin_output:
        k = int(math.log2(cipher.q))
        output = [[0 if c == '0' else 1 for c in np.binary_repr(n, width=k)] for n in output]
    return np.array(output).flatten()

def decrypt(priv_key, input_arr, bin_input=False):
    #print("In decrypt.")
    #priv_key = np.load(priv_key_file, allow_pickle=True)
    #print("priv_key = " + str(priv_key))
    cipher = Cipher(int(priv_key['N']), int(priv_key['p']), int(priv_key['q']))
    #print("got cipher.")
    #print("priv_key['f'] = " + str(priv_key['f']))
    #print(str(priv_key['f'][::-1]))
    cipher.f_poly = Poly(priv_key['f'].astype(np.int)[::-1], x).set_domain(ZZ)
    #print("got f_poly.")
    cipher.f_p_poly = Poly(priv_key['f_p'].astype(np.int)[::-1], x).set_domain(ZZ)
    #print("got f_p_poly.")
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

#def invalid_ciphertext(ct1, ct2):
#    return len(ct1)!=len(ct2) or div(mpfr(str(int(ct1, 16))),mpfr((str(int(ct2, 16))))) != 1.0

def get_password():
    with open("password.txt") as file:
        password = "".join(file.readlines()).strip()
    return password

def main():

    # Start by getting password
    password = get_password()
    #print("The password is " + str(password))
    #root = logging.getLogger()
    #gmpy2.get_context().precision=1000
    #root.setLevel(logging.DEBUG)
    #ch = logging.StreamHandler(sys.stdout)
    #ch.setLevel(logging.DEBUG)
    #ch.setLevel(logging.INFO)
    #ch.setLevel(logging.WARN)
    #root.addHandler(ch)

    #poly_input = False
    #poly_output = False
    input_arr, output = None, None
    
    print("**********      B E Y O N D   Q U A N T U M      **********\n")
    print("   I heard that quantums are flying around these days and")
    print("people are thinking of attacking cryptosystems with them.")
    print("So I found this awesome cryptosystem that is safe from")
    print("quantums! You can send as many qubits as you like at this")
    print("cipher, and none of them will break it. Here is a proof of")
    print("concept to show the world how robust our cryptosystem is.")
    print("I\'ve encrypted a password and no amount of skullduggery")
    print("will help you to get it back. See, you can encrypt and")
    print("decrypt all you want, you won\'t get anywhere!")

    private_key, public_key = generate(N=167, p=3, q=128)#, priv_key_file=priv_key_file, pub_key_file=pub_key_file)
    print("   This is an asymmetric cryptosystem so here is the public")
    print("key:\n")
    print(str(public_key) + "\n")
    pwd_ct = encrypt_command(password.encode(), public_key)
    print("   The password ciphertext is " + pwd_ct + "\n")
    print("   Have at it!\n")

    while True:
        print("/------------------------------\\")
        print("|           COMMANDS           |")
        print("|                              |")
        print("|   encrypt <plaintext>        |")
        #print("   execute <ciphertext> <command>")
        print("|   decrypt <ciphertext>       |")
        print("|   solve_challenge <password> |")
        print("|   exit                       |")
        print("\\------------------------------/\n")
        print("> ", end="")
        sys.stdout.flush()
        parts = sys.stdin.readline()[:-1].split(" ")

        try:
            if parts[0] == "encrypt":
                pt = parts[1]
                #print("About to encrypt.")
                print("\n" + encrypt_command(bytes.fromhex(pt), public_key) + "\n")
                #print("command encrypted.")
                sys.stdout.flush()
            elif parts[0] == "decrypt":
                ct = parts[1]
                #print("ct = " + str(ct))
                #print("   ct class = " + str(ct.__class__))
                #print("pwd_ct = " + str(pwd_ct))
                #print("   pwd_ct_class = " + str(pwd_ct.__class__))
                if ct == pwd_ct:
                    print("\nHey, you tried to decrypt the password ciphertext. That's illegal.")
                    sys.stdout.flush()
                    raise Exception()
                else:
                    #command = bytes.fromhex(parts[2])
                    decrypted = decrypt_command(bytes.fromhex(ct),private_key)
                    print("\n"+ decrypted.decode() + "\n")
                #if command not in decrypt_command(ct, private_key) or invalid_ciphertext(encrypt_command(command, public_key), parts[1]):
                #    raise Exception()
            elif parts[0] == "solve_challenge":
                candidate_password = parts[1]
                #print("candidate_password = " + str(candidate_password))
                #print("   with class " + str(candidate_password.__class__))
                #print("password = " + str(password))
                #print("   with class " + str(candidate_password.__class__))
                if candidate_password == password:
                    print("\nWhat?! How did you do that??\n")
                    with open("flag.txt") as file:
                        print("".join(file.readlines()))
                else:
                    print("\nNope!\n")
            elif parts[0] == "exit":
                print("\nBye!")
                sys.stdout.flush()
                return
            else:
                print("\nUnknown command.")
                raise Exception()
        except:
            print("\nSomething went wrong...")
            print("...try again?\n")
            sys.stdout.flush()
    
if __name__ == "__main__":
    main()
