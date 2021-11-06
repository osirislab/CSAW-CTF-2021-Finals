Most malware writers use this technique to compute the imports (not only for shellcode but also for malware executables).


The challenge is a hex-ed shellcode xored with 0x29 (it's visually obvious what the key is). As any shellcode it is position independent and variables are referred by an offset to the beginning.

It checks the BeingDebugged flag from PEB and, if the process is debugged, it jumps to a location and starts executing from there until it crashes (so it's not immediately obvious that's anti-debugging).
It searches for the GetUserNameA function from the advapi32.dll library starting from PEB. In order to do that it enumerates all loaded modules from PEB, converts the name to lower-case ascii and computes a hash used by the trickbot malware loader for the same purpose. if the hash matches with the hash I hardcoded, then it gets advapi's address and starts parsing advapi for the exported functions. In order to find the function, it enumerates the exported functions and computes the hash until it matches the hardcoded one. In the end, it uses the function to obtain the username on the system on which the shellcode is executed. This is the flag.

They can statically analyze the code, in which case they'll need to understand PEB, PE format, hashes.
Or they can debug the shellcode. One of the ways in which they could debug it is by opening a 32-bit executable in a debugger and copying the shellcode at entry point. If the advapi32.dll library is already loaded in that process, they'll just observe when they get to it. Otherwise they'll need to compute the hash for dlls from system32 to figure out which dll the shellcode is looking for. They'll need to make sure the section the shellcode is executing from has Full Access (it can be added from the debugger, of course).

The python implementation of the hash function is in [hash_function.py](./hash_function.py)

This is the assembly code with comments and labels:

call @start
@str:
  DB 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  DB 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  DB 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
@advapi_funcs:
  DB 0x1
@advapi_hash:
  DD 0xdedc9aff
@advapi_GetUserNameA_hash:
  DD 0x54b99a8f
@start:
pop edx
; prepare stack
mov esp, edx
sub esp, 0x1000
; align stack
and esp, 0xffffff00
; get PEB
mov ecx, fs:[30]
test ecx, ecx
jz @end
; check BeingDebugged flag from PEB
cmp byte ptr [ecx+2], 0
jne @random_location
; PEB->Ldr=PEB_LDR_DATA
mov ecx, [ecx+0x0C]
test ecx, ecx
jz @end
; PEB_LDR_DATA->InMemoryOrderModuleList
mov ebx, [ecx+0x14]
test ebx, ebx
jz @end
add ecx, 0x14
cmp ecx, ebx
jz @end
@dll_loop:
@random_location:
; LDR_DATA_TABLE_ENTRY->BaseDllName
push [ebx+0x28]
call @unicode_to_lower_ascii
add esp, 4
push edx
call @compute_checksum
add esp, 4
cmp eax, [edx+0x31]
jz @dll_loop_end
mov ebx, [ebx]
cmp ecx, ebx
jz @end
jmp @dll_loop
@dll_loop_end:
; LDR_DATA_TABLE_ENTRY->DllBase
mov ebx, [ebx+0x10]
; search kernel function addrs
movzx ecx, byte ptr [edx+0x30]
@func_loop:
mov edi, edx
add edi, 0x31
add edi, ecx
add edi, ecx
add edi, ecx
add edi, ecx
mov esi, [edi]
push esi
push ebx
call @get_func_addr
add esp, 8
mov dword ptr [edi], eax
dec ecx
cmp ecx, 0
jnz @func_loop
call @get_username
jmp @end

; compute_checksum function
@compute_checksum:
push ebp
mov ebp, esp
pushad
mov ecx, [ebp+0x08]
xor edx, edx
xor eax, eax
@compute_check_loop:
movsx esi, byte ptr [ecx]
test esi, esi
jz @compute_check_loop_end
add esi, edx
mov edi, esi
shl edi, 5
shl edi, 5
add edi, esi
mov edx, edi
shr edx, 5
shr edx, 1
xor edx, edi
inc ecx
jmp @compute_check_loop
@compute_check_loop_end:
lea eax, [edx+edx*8]
mov ecx, eax
shr ecx, 0x0B
xor ecx, eax
mov eax, ecx
shl eax, 0x0F
add eax, ecx
mov [esp+0x1C], eax
popad
mov esp, ebp
pop ebp
ret

; unicode_to_lower_ascii function
@unicode_to_lower_ascii:
push ebp
mov ebp, esp
pushad
mov esi, [ebp+0x08]
xor ecx, ecx
@unicode_to_ascii_loop:
mov ax, word ptr [esi]
test ax, ax
jz @unicode_to_ascii_loop_end
or al, 0x20
mov [edx], al
add esi, 2
inc edx
jmp @unicode_to_ascii_loop
@unicode_to_ascii_loop_end:
mov byte ptr [edx], 0x00
popad
mov esp, ebp
pop ebp
ret

; get_func_addr function
@get_func_addr:
push ebp
mov ebp, esp
pushad
sub esp, 0x18
; get lib address
mov edi, [ebp+0x08]
test edi, edi
jz @get_func_addr_ret_zero
; get func hash
mov edx, [ebp+0x0C]
; IMAGE_DOS_HEADER.e_lfanew
mov ecx, [edi+0x3C]
; export data directory virtual address
; IMAGE_NT_HEADERS32.OptionalHeader.DataDirectory[0].VirtualAddress
mov eax, [edi+ecx+0x78]
test eax, eax
jz @get_func_addr_ret_zero
; export data directory size
; IMAGE_NT_HEADERS32.OptionalHeader.DataDirectory[0].Size
cmp dword [edi+ecx+0x7C], 0x00
jz @get_func_addr_ret_zero
; export data directory address
lea ecx, [edi+eax]
; IMAGE_EXPORT_DIRECTORY structure
mov [esp], ecx
; IMAGE_EXPORT_DIRECTORY.AddressOfFunctions
mov ecx, [edi+eax+0x1C]
add ecx, edi
mov [esp+0x04], ecx
; IMAGE_EXPORT_DIRECTORY.AddressOfNames
mov ecx, [edi+eax+0x20]
add ecx, edi
mov [esp+0x08], ecx
; IMAGE_EXPORT_DIRECTORY.AddressOfNameOrdinals
mov ecx, [edi+eax+0x24]
add ecx, edi
mov [esp+0x0C], ecx
; IMAGE_EXPORT_DIRECTORY.NumberOfNames
mov eax, [esp]
cmp dword [eax+0x18], 0
jz @get_func_addr_ret_zero
xor ebx, ebx
@next_func_name:
mov eax, [esp+0x08]
mov ecx, [eax+ebx*4]
cmp byte ptr [edi+ecx], 0x00
jz @goto_next_func_name
lea eax, [edi+ecx]
push eax
call @compute_checksum
add esp, 4
cmp eax, edx
jnz @goto_next_func_name
mov eax, [esp+0x0C]
movzx ecx, word ptr [eax+ebx*2]
mov eax, [esp+0x04]
mov eax, dword ptr [eax+ecx*4]
add eax, edi
jmp @get_func_addr_ret
@goto_next_func_name:
inc ebx
jmp @next_func_name
@get_func_addr_ret_zero:
xor eax, eax
@get_func_addr_ret:
add esp, 0x18
mov [esp+0x1C], eax
popad
mov esp, ebp
pop ebp
ret

@get_username:
push ebp
mov ebp, esp
pushad
sub esp, 0x4
mov dword ptr [esp], 0x10
push esp
push edx
call [edx+0x35]
add esp, 0x4
mov [esp+0x1C], eax
popad
mov esp, ebp
pop ebp
ret

@end:
nop
nop
nop
nop
nop
nop
nop
nop
