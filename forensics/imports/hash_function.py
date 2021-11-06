def compute_checksum(string):
    edx = 0
    for char in string:
        esi = ord(char) + edx
        edi = ((esi << 10) + esi) & 0xFFffFFff
        edx = (edi >> 6) ^ edi
    eax = (edx + edx * 8) & 0xFFffFFff
    ecx = (eax >> 11) ^ eax
    eax = (ecx + (ecx << 15)) & 0xFFffFFff
    return eax
