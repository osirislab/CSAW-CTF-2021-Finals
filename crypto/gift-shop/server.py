
import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode, b64decode
import reuse
import sys
# pip3 install pycryptodome reuse


key = b'0123456789abcdef'
used_ivs = set()

# Components to the poodle:
# 1. User enters text A
# 2. User enters text B

# Encryption:
# 3. Server encrypts (text A + flag + text B + hmac of message) and adds padding
# 4. I need an hmac function
# 5. I need a padding function

# Decryption:
# 6. Server checks padding and removes it
# 7. Server checks hmac
# 8. Server decrypts message with key
# 9. Server says "Printing your decrypted message is still TODO" or the like

# Implementation: 
# x 1. Have server read a flag from disk and print it
# x 2. Have server take input A and input B from user and print the message
# x 3. Have server take hmac of the message
# x 4. Write and test a function where the server checks the hmac of the message
# x 5. Encrypt the message using AES-256-CBC
# x 6. Write and test decrypting the message using AES-256-CBC
# x 7. Add padding to the message and base64 encode it
# x 8. Write and test base64 decoding and removing padding from the message
# x 9. Write a story intro and menu options in which the user can encrypt a message or decrypt a message, with a loop
# 10. Develop a simple POODLE exploit and save it to a separate "original_solver.py" file
# 11. Provide prices for each of my 16 store objects
# 12. Create a menu interface for the store
# 13. Adjust the way the message gets printed
# 14. In the solver, write an algorithm to make your balance be a specific length
# 15. In the solver, write an algorithm to make your object purchased length be a specific length
# 16. Combine 14 and 15: in the solver, write an algorithm to make the original text A be a specific length and text B be a specific length
# 17. Use #16 and modify original_solver.py to make the POODLE attack work for the new store
# 18. Make sure the story looks good
# 19. Polish the spacing etc.
# 20. Deliver for testing

def read_flag():
    with open("flag.txt") as f:
        return f.readline().strip()

def get_hmac(m):
    return hmac.new(key, msg=m, digestmod=hashlib.sha256).digest()

def hmac_is_valid(pt):
    digest = pt[-32:]
    msg = pt[:-32]
    #print("msg class: " + str(msg.__class__))
    return equal_bytearrays(hmac.new(key, msg=msg, digestmod=hashlib.sha256).digest(), digest)

def equal_bytearrays(a1, a2):
    if len(a1)!=len(a2):
        return False
    else:
        for i in range(len(a1)):
            if a1[i]!=a2[i]:
                return False
        return True

def pad(pt):
    pad_value = 16 - len(pt)%16
    pt = pt + (chr(pad_value)*pad_value).encode()
    return pt

def verify_padding_and_unpad(pt):
    pad_value = pt[-1]
    print("pad_value = " + str(pad_value))
    if pad_value == 0 or pad_value > 16:
        return False
    else:
        pt = pt[:(-1*pad_value)]
        return pt

def encrypt(pt):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pt)
    #print("In encrypt: class of ct = " + str(ct.__class__))
    #print("      ct = " + str(ct))
    #print("      len(ct) = " + str(len(ct)))
    ct = iv + ct 
    ct = b64encode(ct)
    #print("In encrypt: class of ct = " + str(ct.__class__))
    #print("      ct = " + str(ct))
    #print("      len(ct) = " + str(len(ct)))
    return ct

def decrypt(ct):
    #print("In decrypt: class of ct = " + str(ct.__class__))
    #print("      ct = " + str(ct))
    #print("      len(ct) = " + str(len(ct)))
    ct = b64decode(ct)
    #print("In decrypt: class of ct = " + str(ct.__class__))
    #print("      ct = " + str(ct))
    #print("      len(ct) = " + str(len(ct)))
    iv = ct[:16]
    if iv in used_ivs:
        print("Warning: detected repeated use of an IV during decryption. Something suspicious is going on. Program will exit.")
        exit(0)
    else:
        used_ivs.add(iv)
        ct = ct[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = cipher.decrypt(ct)
        #print(b"In decrypt: pt = " + pt)
        return pt

def decrypt_and_verify(ct):
    pt = decrypt(ct)
    ## Unit test: change last padding.
    #print("Unit test: change last padding.")
    #print(b"pt = " + pt)
    #print("Last padding = " + str(pt[-1]))
    #pt = pt[:-1]+chr(pt[-1]+1).encode()
    #print(b"pt = " + pt)
    # Invalid hmac, great.

    # Unit test: change padding to invalid number (tested 17 and 0).
    #print("Unit test: change last padding.")
    #print(b"pt = " + pt)
    #print("Last padding = " + str(pt[-1]))
    #pt = pt[:-1]+chr(pt[-1]+16).encode()
    #print(b"pt = " + pt)
    # Invalid padding, great.

    #print("Unit test: change last padding.")
    #print(b"pt = " + pt)
    #print("Last padding = " + str(pt[-1]))
    #pt = pt[:-1]+chr(0).encode()
    #print(b"pt = " + pt)
    # Invalid padding, great.
    pt = verify_padding_and_unpad(pt)
    valid_plaintext = True
    if pt:
        if not hmac_is_valid(pt):
            valid_plaintext = False
            #print("(Testing): invalid hmac.")
    else:
        valid_plaintext = False
        #print("(Testing): invalid padding.")
    if valid_plaintext:
        print("Valid plaintext. We assume you have purchased our flag decryption key and can therefore read the flag. Thank you for your patronage.")
        #print("pt class = " + str(pt.__class__))
        #print(b"The message is: " + pt[:-32])
    else:
        print(b"Something went wrong during decryption. Try again?")
    return

#def encrypt(key, plain, IV):
#    cipher = AES.new( key.decode('hex'), AES.MODE_CBC, IV.decode('hex') )
#    return IV + cipher.encrypt(plain).encode('hex')

#def decrypt(key, ciphertext, iv):
#    cipher = AES.new(key.decode('hex'), AES.MODE_CBC, iv.decode('hex'))
#    return cipher.decrypt(ciphertext.decode('hex')).encode('hex')

def process_encryption(flag):
    input_a = input("Enter input_a: ").encode()
    input_b = input("Enter input_b: ").encode()
    #print("input_a = " + str(input_a))
    #print("input_a.class = " + str(input_a.__class__))
    msg = b"Here\'s your beautiful flag that you just bought for " + input_a + b" bitcoins: " + flag + b". Aren\'t you glad you didn\'t buy a bunch of useless items like " + input_b + b"(s) instead?"
    #print("The message is: " + str(msg))
    hmac = get_hmac(msg)
    #print("The hmac is " + str(hmac))
    pt = msg + hmac
    #print(b"The new message is " + pt)
    #print("Is the hmac valid? " + str(hmac_is_valid(pt)))
    pt = pad(pt)
    ct = encrypt(pt)
    print(b"A plane flies overhead flying a banner that reads: " + ct)

def main():

    print("**********      C S A W   G I F T   S H O P      **********\n")
    print("\n")
    print("   Welcome to the CSAW Gift Shop! We're holding it outside")
    print("this year due to the pandemic. But we have a plethora of")
    print("useful items here to suit your taste, as well as encrypted")
    print("flags constantly flying overhead and a key to decrypt them")
    print("that should be well within your price range.\n")

    flag = read_flag().encode()
    #print("The flag is " + str(flag))

    while True:
        print("")
        print("Enter your choice: ")
        print("1) Give me two inputs and encrypt")
        print("2) Decrypt")
        print("3) Exit")
        
        try:
            selection = int(input("> ").strip())
            #print("User input = " + str(user_input))
            #print("User input class = " + str(user_input.__class__))
            #selection = int(user_input)
            if selection == 1:
                process_encryption(flag)
                sys.stdout.flush()
            elif selection == 2:
                ct = input("Enter the base64-encoded ciphertext to decrypt: ")
                #print("ct = " + str(ct))
                #print("ct class = " + str(ct.__class__))
                ct = ct.encode()
                #print("ct = " + str(ct))
                #print("ct class = " + str(ct.__class__))
                decrypt_and_verify(ct)
                sys.stdout.flush()
                ## Unit test: change padding to a wrong byte.
                #ct = b64decode(ct)
                #print(b"ct = " + ct)

                #decrypt_and_verify(b64encode(ct))
                # Works, great.
                #print(str(ct[-1].__class__))

                ## Unit test: decrypt twice with same IV.
                #print("Decrypting again.")
                #decrypt_and_verify(ct)
                # Fails, perfect.

                #pt2 = decrypt(ct)
                #print(b"pt2 = " + pt2)
            elif selection == 3:
                print("Thank you for shopping with CSAW!")
                exit(0)
            else:
                print("Error: invalid menu option.")
                raise Exception
        except Exception as ex:
            print("\nSomething went wrong...")
            print("...try again?\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
