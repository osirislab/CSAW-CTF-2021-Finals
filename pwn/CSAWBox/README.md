# Author

n132/xm2146

# Note
It's a challenge about VM escaping: a binary runs in the VM and people are supposed to use two vulnerabilities to escape from the VM.
It's easy if you know the solution, that's from an unexcepted solution in 0CTF-finial. If you are testing this challenge, please help me check if the VM is secure and doesn't have other vulnerabilities and people could not use the vulnerability perform some easy solutions, which means finding an easier way is harder than using the official solution.
Any problem please contact xm2146@nyu.edu

# Vulnerabilities
* Buffer overflow in VM(./src/main.c) function `readint`
* Buffer overflow in binary, CSAW-Game. function `check`
# Solution

* Use BoF in check to perform ROP to trigger VM vulnerability
* back to binary after freeing `tcahce_perthread_struct`
* Partial write + Use binmap as the head of chunk
* Use tacheche-key to bypass a crash in strtol
* IO Leak + `__free_hook` hijack

