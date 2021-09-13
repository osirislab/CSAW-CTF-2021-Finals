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
It shows how cached accesses take 4 ticks, while uncached takes 8.
