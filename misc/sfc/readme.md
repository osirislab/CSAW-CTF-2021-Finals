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
