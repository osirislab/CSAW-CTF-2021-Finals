#0e rbp 0f rsp
#07 sub 02 add byte
#04 rsi \ 05 rdi 
#gadget
from pwn import *
head =b"\x24\x0e\x1b\x0e\x0f"
leave_ret=b'\x1b\x0f\x0e\x25\x0e\x28'
PUTS=b'\x2d'
def store_a_number(offset,num):
	res=f'\x1b\x00\x0e\x07\x00{chr(offset)}'.encode()
	res+=b'\x30\x00'+p8(num)
	return res
def sub_rsp(num):
	return f'\x07\x0f{chr(num)}'.encode()
def store_value_to_varible(offset,reg,length=4):
	if(length==4):
		res=f'\x1b\x01\x0e\x07\x01{chr(offset)}\x30\x01{chr(reg)}'.encode()
	return res
def load_varible_from_stack(offset,regs,length=4):#mov     edx, [rbp+var_4]
	if(length==4):
		res= f'\x07\x0e{chr(offset)}\x36{chr(regs)}\x0e\x02\x0e{chr(offset)}'.encode()
	elif(length==8):
		res= f'\x07\x0e{chr(offset)}\x37{chr(regs)}\x0e\x02\x0e{chr(offset)}'.encode()
	return res
def jmp(t,gap):
	if t == 'jmp':
		return b'\x11'+p16(gap)
	elif t =='jz':
		return b'\x12'+p16(gap)
	elif t=='ja':
		print("Hit")
		return b'\x14'+p16(gap)
	elif t=='jnz':
		return b'\x13'+p16(gap)
	
def add_regs(reg1,reg2):
	return f'\x01{chr(reg1)}{chr(reg2)}'.encode()
def deref_reg(reg1,reg2,length=1):
	if(length==1):
		return f'\x34{chr(reg1)}{chr(reg2)}'.encode()
def test_reg(reg):
	return f'\x38{chr(reg)}'.encode()
def do_write(reg):#reg means the paremater, should be a address 
	return f'\x1b\x04{chr(reg)}\x2c'.encode()
def varible_add(offset,num,length=4):# rbx 
	if(length==4):
		res = f'\x07\x0e{chr(offset)}\x36\x01\x0e\x02\x01{chr(num)}\x02\x0e{chr(offset)}'.encode()
	return res
def set_reg(reg,num):
	return f'\x1c{chr(reg)}{chr(num)}'.encode()
def read_int():
	return b'\x2a\x00'
def mov_qword(reg,num):
	return f"\x1f{chr(reg)}{chr(num)}".encode()
def cmp_reg_num(reg,num):
	return b'\x08'+p8(reg)+p16(num)

def cmp_reg_large_num(reg,num):
	return b'\x0a'+p8(reg)+p64(num)
def call(address):
	return b'\x27'+p16(address)

RO=b''
LengthOfMessage=len(RO)
RO =b'LengthOfMessage:\0'
Content=len(RO)
RO+=b'Content:\0'
Escape=len(RO)
RO+=b"Escape from the CSAW-box?\0"
Out_there=len(RO)
RO+=b"Out there, you don't stand a chance. I believe you will be back soon!\0"
Logo_add =len(RO)
RO+=b"  ______    ______    ______   __       __  __   ______     __   \n"
RO+=b" /      \\  /      \\  /      \\ /  |  _  /  |/  | /      \\  _/  |  \n"
RO+=b"/$$$$$$  |/$$$$$$  |/$$$$$$  |$$ | / \\ $$ |$$/ /$$$$$$  |/ $$ |  \n"
RO+=b"$$ |  $$/ $$ \\__$$/ $$ |__$$ |$$ |/$  \\$$ |$/  $$____$$ |$$$$ |  \n"
RO+=b"$$ |      $$      \\ $$    $$ |$$ /$$$  $$ |     /    $$/   $$ |  \n"
RO+=b"$$ |   __  $$$$$$  |$$$$$$$$ |$$ $$/$$ $$ |    /$$$$$$/    $$ |  \n"
RO+=b"$$ \\__/  |/  \\__$$ |$$ |  $$ |$$$$/  $$$$ |    $$ |_____  _$$ |_ \n"
RO+=b"$$    $$/ $$    $$/ $$ |  $$ |$$$/    $$$ |    $$       |/ $$   |\n"
RO+=b" $$$$$$/   $$$$$$/  $$/   $$/ $$/      $$/     $$$$$$$$/ $$$$$$/ \n"
RO+=b"                                                                 \n"
RO+=b"                                                                 \n"



data =b''
# main #0
data+=head
data+=set_reg(0,0)
data+=call(272)#logo
data+=set_reg(0,0)
data+=call(236)#vul
data+=set_reg(0,0)
data+=b"\x99"
# main end
print("Function PUTS:",len(data))
# puts #
data+=head
data+=sub_rsp(0x20)
data+=b"\x1b\x00\x0e\x07\x00\x18\x31\x00\x05"
data+=b'\x1c\x05\x00'
data+=store_a_number(4,0)

pin_0 = len(data)
print(" Pin_0:",len(data))
data+=load_varible_from_stack(4,3,4)
data+=load_varible_from_stack(18,0,8)
data+=add_regs(0,3)
data+=deref_reg(0,0,1)
data+=test_reg(0)
pin_1 = len(data)+3
print(" Pin_1:",len(data))
data+=jmp('jz',116+3)#
data+=load_varible_from_stack(4,3,4)
data+=load_varible_from_stack(18,0,8)
data+=add_regs(0,3)
data+=do_write(0)
data+=varible_add(4,1,4)
pin_2 = len(data)+3
print(" Pin_2:",len(data))
data+=jmp("jmp",50)
data+=leave_ret
# puts end
pin_add =len(data)

# add
data+=head
data+=sub_rsp(0x10)
data+=set_reg(0x5,LengthOfMessage)
data+=PUTS
data+=set_reg(0x0,0)
data+=read_int()
data+=store_value_to_varible(4,0,4)
data+=cmp_reg_num(0,0x887)
data+= jmp('ja',172)#
data+= load_varible_from_stack(4,0,4)
data+= b'\x1b\x04\x00'
data+= b'\x39\x3a'
pin_4= len(data)
print("Pin_4:",len(data))
data+=leave_ret
# add end


pin_check=len(data)
#check
data+=head
data+=sub_rsp(0x30)
data+=b'\x1b\x00\x0e\x07\x00\x30'#lea     rax, [rbp+buf]
data+=b'\x1b\x05\x00\x1c\x04\x48\x2b'# read(0,rax,0x48)
data+=load_varible_from_stack(0x30,0,8)#lea     rax, [rbp+buf]
data+=b'\x00\x00\x00'
data+=cmp_reg_large_num(0,0xdeadbeefcafebabe)
data+=set_reg(0,1)
data+=jmp('jz',230)
data+=set_reg(0,0)
print(" pin_5",len(data))
data+=leave_ret
#check end
print("Function Vul:",len(data))
#vul
data+=head
pin_5=len(data)
data+=set_reg(0,0)
data+=call(pin_add)#add
data+=set_reg(0x5,Escape)
data+=PUTS
data+=set_reg(0x0,0)
print(" Pin_6",len(data))
data+=call(pin_check)
data+=test_reg(0)
pin_6=len(data)+3
data+=jmp('jnz',pin_5)
data+=set_reg(0x5,Out_there)
data+=PUTS
data+=leave_ret
#vul end
print("Function logo:",len(data))
#print(pin_logo)
#logo 
data+=head
data+=set_reg(0x5,Logo_add)
data+=PUTS
data+=leave_ret
#logo end


with open("./CSAW-GAME",'wb') as f:
	f.write(data.ljust(0x1000,b'\0')+RO.ljust(0x1000,b'\0'))
