
# Beyond Quantum

This challenge demonstrates the malleability of the NTRU algorithm. I've used an implementation by Jedrzej Krause (https://github.com/jkrauze/ntru) with his permission.

Here's how it works:

The player interacts with a server and gets the `server.py` file. They also get the contents of the `cipher` folder, which is Krause's implementation of the NTRU algorithm. I've gotten rid of the logging that he provides, as well as the part that pads the ciphertext. Basically the challenge is a take on the traditional signature forgery challenge -- except here you're doing a chosen ciphertext attack. The idea is you take the ciphertext and slightly modify it, and that produces a change in the plaintext that can be in the padding area. So "cat flag.txt", if you modify the ciphertext in the middle, becomes unrecognizable, but if you add a bit to the very end it still decrypts to "cat flag.txt" plus some trailing bytes. So you get the flag if you manage to encrypt "flag.txt", modify the ciphertext, and have the result decrypt to "flag.txt" plus some garbage. It's pretty easy and intended just to demo the malleability of NTRU -- so more instructive than challenging. 

To keep people from completely cheesing the challenge by entering "flag.txta" or "laskdfj flag.txt" and still being able to get the flag that way, I do two things: a length check that the ciphertext doesn't change in length, and I do a high-precision division of the original ciphertext and the modified ciphertext, to make sure the first 250 or so digits in the ciphertext are all the same. The division isn't high enough precision to check the last 50 digits, though. So, that at least forces people to modify the ciphertext. Like I say, pretty easy for finals though. With the ZipCrypto first part this would have been a 200-point quals challenge I'd say, so a 100-point challenge for finals, sure.

The Dockerfile is Ubuntu 20.04 because I install `gmpy2` to do the high-precision division. The container also requires write access to produce a random polynomial, public key, and private key when the challenge is run. 

TODO: Testing question: what happens when multiple users run this challenge simultaneously? I want to make sure we don't get different public / private keys written to the Docker container. 
