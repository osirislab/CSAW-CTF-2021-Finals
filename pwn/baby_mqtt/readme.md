## baby\_mqtt

MQTT client program, 32 bits x86 binary, No PIE.

Given the challenge binary (strip??), libc.so, and Dockerfile.

Added one bug through the Chaff Bug, with controlled 4 bytes write to the return address.
Originally set the constraint, so that you could only look for ROP gadgets within the challenge
binary (0x0804xxxx), but I didn't find good gadgets... so for now, I changed the constraint, so
the you are able to look for gadgets in libc library. libc address is always loaded roughly at
0xf75xx000. Need to brute force ~1 byte. There shouldn't the one gadget in 32bit libc, so the
my solution is to find a stack pivot gadget, and get shell.

There'll be another chaffed version of this MQTT client as a follow-up.
