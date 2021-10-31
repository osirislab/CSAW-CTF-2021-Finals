#0e rbp 0f rsp
#gadget
push_rbp_move_rbp_rsp=b"\x24\x0e\x23\x0e\x0f"
sub_rsp_n=b'\x07\x0e{}'
mov_rbp_offset_num=b'\x1b\x00\x0e\x07\x00{}\x1b\x0e\x00'# move rax,rbp; sub rax,n; mov [rax],num

data =b''
#read int
data+=push_rbp_move_rsp_rbp
data+=sub_rsp_n.format(0x20)
data+=mov_rbp_offset_num




with open("./CSAW-GAME",'rb') as f:
	f.write(data)
assert(len(data)<0x1000);
