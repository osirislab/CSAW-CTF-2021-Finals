#0e rbp 0f rsp
#07 sub 02 add byte
#04 rsi \ 05 rdi 
#gadget
store_parameter = b'\x1b\x00\x0e\x07\x00{}\x31\x00\x05'#mov     [rbp+var_18], rdi
head =b"\x24\x0e\x23\x0e\x0f"
leave_ret=b'\x1b\x0f\x0e\x25\x0e\x28'
PUTS=b'\x2d'
def store_a_number(offset,num):
	res=b'\x1b\x00\x0e\x07\x00{}'.format(offset)
	res+=b'\x30\x00'+p8(num)
	return res
def sub_rsp(num):
	return b'\x07\x0f{}'.format(num)
def store_value_to_varible(offset,reg,length=4):
	if(length==4):
		res=b'\x1b\x01\x0e\x07\x01{}\x30\x01{}'.format(offset,reg)
	return res
def load_varible_from_stack(offset,regs,length=4):#mov     edx, [rbp+var_4]
	if(length==4):
		res= b'\x07\x0e{}\x36\x{}\x0e\x02\x0e{}'.format(offset,regs,offset)
	elif(length==8):
		res= b'\x07\x0e{}\x37\x{}\x0e\x02\x0e{}'.format(offset,regs,offset)
	return res
def jmp(t,gap):
	h = gap >>0x8
	l = gag % 0x100; 
	if t == 'jmp':
		return b'\x11{}{}'.format(h,l)
	elif t =='jz':
		return b'\x12{}{}'.format(h,l)
	elif t=='ja':
		return b'\x14{}{}'.format(h,l)
def add_regs(reg1,reg2):
	return b'\x01{}{}'.format(reg1,reg2)
def deref_reg(reg1,reg2,length=1):
	if(length==1):
		return b'\x34{}{}'.format(reg1,reg2)
def test_reg(reg):
	return b'\x38{}'.format(reg)
def do_write(reg):#reg means the paremater, should be a address 
	return b'\x1b\x04{}\x2c'.format(reg)
def varible_add(offset,num,length=4):# rbx 暂存
	if(length==4):
		res = b'\x07\x0e{}\x36\x01\x0e\x02\x01{}\x02\x0e{}'.format(offset,num,offset)
	return res
def set_reg(reg,num):
	return b'\x1c{}{}'.format(reg,num)
def read_int():
	return b'\x2a\x00'
def mov_qword(reg,num):
	return b"\x1f{}{}".format(reg,p64(num))
def cmp_reg_num(reg,num):
	return '\x08{}{}'.format(reg,p16(num))
RO=b''
LengthOfMessage=len(RO)
RO =b'LengthOfMessage:\0'
Content=len(RO)
RO+=b'Content:\0'

data =b''
# puts
data+=head
data+=sub_rsp(0x20)
data+=store_parameter.format(0x18)
data+=b'\x1c\x05\x00'
data+=store_a_number(4,0)
pin_0 = len(data)
data+=load_varible_from_stack(4,3,4)
data+=load_varible_from_stack(18,0,8)
data+=add_regs(0,3)
data+=deref_reg(0,0,1)
data+=test_reg(0)
pin_1 = len(data)+3
data+=jmp('jz',pin_2-pin_1)
data+=load_varible_from_stack(4,3,4)
data+=load_varible_from_stack(18,0,8)
data+=add_regs(0,3)
data+=do_write(0)
data+=varible_add(4,1,4)
pin_2 = len(data)+3
data+=jmp("jmp",pin_2-pin_0)
data+=leave_ret
# puts end
# add
data+=head
data+=sub_rsp(0x10)
data+=set_reg(0x5,LengthOfMessage)
data+=PUTS
data+=set_reg(0x0,0)
data+=read_int()
data+=store_value_to_varible(4,0,4)
data+=cmp_reg_num(0,0x887)
pin_3 = len(data)+3
data+= jmp('ja',pin_4-pin_3)
data+= load_varible_from_stack(4,0,4)
data+= b'\x1b\x04\x00'
data+= b'\x39\x3a'
pin_4= len(data)
data+=leave_ret
# add end
#check
data+=head
data+=sub_rsp(0x30)
data+=b'\x1b\x00\x04\x07\x00\x30'#lea     rax, [rbp+buf]
data+=b'\x1b\x05\x00\x1c\x04\x48\x2b'# read(0,rax,0x48)
data+=load_varible_from_stack(0x30,0,4)#lea     rax, [rbp+buf]
data+=cmp_reg_num(0,0xdeadbeefcafebabe)
data+=set_reg(0,1)
data+=jmp('jz',3)
data+=set_reg(0,0)
data+=leave_ret
#check end
#vul
data+=head
data+=set_reg(0,0)
data+=call??
data+=set_reg(0x5,??)
data+=PUTS
data+=set_reg(0x0,0)
data+=call??
data+=test_reg(0)
data+=jmp('jnz'??)
data+=set_reg(0x5,??)
data+=PUTS
data+=leave_ret
#vul end
#logo 
data+=head
data+=set_reg(0x5,??)
data+=PUTS
data+=set_reg(0x5,??)
data+=PUTS
data+=set_reg(0x5,??)
data+=PUTS
data+=set_reg(0x5,??)
data+=PUTS
data+=set_reg(0x5,??)
data+=PUTS
data+=set_reg(0x5,??)
data+=PUTS
data+=leave_ret
#logo end
# main
data+=head
data+=set_reg(0,0)
data+=call??#init
data+=set_reg(0,0)
data+=call?? logo
data+=set_reg(0,0)
data+=call??vul
data+=set_reg(0,0)
data+=leave_ret
# main end


with open("./CSAW-GAME",'rb') as f:
	f.write(data.ljust(0x1000,b'\0')+RO.ljust(0x1000,b'\0'))