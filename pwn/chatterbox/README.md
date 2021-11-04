# Chatterbox

Author: cts (@gf_256)

Challenge description:

```
it's a chat server, go pwn it. enough said

```

# Author's notes

This is a Windows heap pwn challenge. I feel like many CTF players are not exposed to Windows before so this will be an interesting challenge for them.

Attached binaries: contents of `public/` . Remote's `ws2_32.dll` and `kernel32.dll` should be provided too to help the CTF players.
**Ideally,** we would give them the VM image too so they can test locally against the exact same environment as remote.

Difficulty: Hard, about 500 points.

# Deployment notes

The server itself is the pwnable, so each team should have its own instance of the server. Crashing the server is expected so each instance should auto-restart immediately.

**Solving the challenge requires spraying many connections to the daemon. So every team needs to be on its own instance.**

If you solve the challenge, there is the possibility of doing some shenanigans like shutting down the VM, so we should hope that the solving teams will respect the sportsmanship.

**Flag should be in C:\flag.txt and be world-readable.**

# Vulnerabilities

1. Heap overflow, attacker can write arbitrarily far out of bounds of a chunk of size 1024 bytes

2. The function `recv_packet` lacks adequate error handling which can lead to an incomplete read if the socket is shut down in one direction only, but not closed. This can be paired with the heartbeat functionality to get an out-of-bounds read for a leak.

3. any unintended bugs I may have made by mistake.

# Exploit strategy

The solve.py exploit is a total mess and not portable, but it suffices for a CTF quality exploit.

1. Spray a bunch of ClientSocket objects onto the heap

2. Out-of-bounds read using Bug #2 to leak some vtable pointers from the sprayed ClientSockets. This gives us leak for Server.exe base address

3. Spray ClientSockets again

4. Use Bug #1 to overflow and overwrite some vtable pointers in the sprayed objects. This step is not reliable and it can just crash.

5. We have a single gadget after overwriting vtable pointer, we use this to stack pivot to the heap

6. Then we stack pivot to the .data section in the "channel topic" buffer that is easily controllable, and at a known constant offset from Server.exe

7. Connectback shellcode that sends the flag. We can't spawn a shell since stdin/stdout aren't dup'd to the socket.
