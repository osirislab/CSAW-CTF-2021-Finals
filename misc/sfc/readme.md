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
