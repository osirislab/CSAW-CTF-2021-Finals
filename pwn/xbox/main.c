#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<stdint.h>
uint64_t page=0x1000;
char *code=0;
char *data=0;
uint64_t regs[0x10]={0};
uint64_t pc=0;
uint64_t msg=0;
uint64_t ins_ct=0x20;
uint64_t rsp=0x800;
uint64_t rbp=0x800;
int64_t FLAG=0;

uint8_t get_byte(){
	uint8_t res=0;
	segfault(pc,1);
	res=code[pc++];
	return res;
}
uint16_t get_word(){
	uint16_t *res=0;
	segfault(pc,2);
	res=(uint16_t*)code[pc];
	pc+=2;
	return *res;
}
uint32_t get_dword(){
	uint32_t *res=0;
	segfault(pc,4);
	res=(uint32_t*)code[pc];
	pc+=4;
	return *res;
}
uint64_t get_qword(){
	uint64_t *res=0;
	segfault(pc,8);
	res=(uint64_t*)code[pc];
	pc+=8;
	return *res;
}
void setflag(uint64_t a,uint64_t b){
	if(a>b)
		FLAG=1;
	else if(a==b)
		FLAG=0;
	else
		FLAG=-1;
}
void register_index(uint64_t idx){
	if(idx>=0x10)
		die("segfault");
}
void segfault(size_t p, size_t move){
	if( p + move >=page)
		die("segfault");
	return 1;
}
void die(char *s){
	printf("%s\n",s);
	exit(1);
}
void init(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	void *buf;
	int f=open("/dev/urandom",O_RDONLY);
	if(f<=0)
		die();
	read(f,&buf,8);
	buf = (long unsigned int)buf & 0xfffffffffffff000;
	mmap((void *)buf,0x3000,3,0x22,0,0);
	close(f);
	code = buf;
	data = code +page;
}
void load(){
	int f=open("./sprite_away",O_RDONLY);
	unsigned int res= read(f,code,0x2000);
	if(res!=0x2000)
		die();
	close(f);
}
void NOP(){
	return;
}
void ADD(uint8_t c){
	uint64_t arg1=0;
	uint64_t arg2=0;
	c-=1;
	switch(c)
	{	
		arg1=(uint64_t)get_byte();
		register_index(arg1);
		case 0://reg + reg
			arg2=(uint64_t)get_byte();
			register_index(arg2);
			regs[arg1]+=regs[arg2];
			break
		case 1://reg + 1 byte
			arg2=(uint64_t)get_byte();
			regs[arg1]+=arg2;
			break;
		case 2://reg + 2 bytes
			arg2=(uint64_t)get_word();
			regs[arg1]+=arg2;
			break;
		case 3://reg + 4 bytes
			arg2=(uint64_t)get_dword();
			regs[arg1]+=arg2;
			break;
		case 4://reg + 4 bytes
			arg2=get_qword();
			regs[arg1]+=arg2;
			break;
	}
}
void SUB(uint8_t c){
	uint64_t arg1=0;
	uint64_t arg2=0;
	c-=6;
	switch(c)
	{	
		arg1=(uint64_t)get_byte();
		register_index(arg1);
		case 0://reg - reg
			arg2=(uint64_t)get_byte();
			register_index(arg2);
			regs[arg1]-=regs[arg2];
			setflag(regs[arg1],regs[arg2])
			break
		case 1://reg - 1 byte
			arg2=(uint64_t)get_byte();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2)
			break;
		case 2://reg - 2 bytes
			arg2=(uint64_t)get_word();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2)
			break;
		case 3://reg - 4 bytes
			arg2=(uint64_t)get_dword();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2)
			break;
		case 4://reg - 4 bytes
			arg2=get_qword();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2)
			break;
	}
}
void MUL(){
	uint64_t arg1=0;
	uint64_t arg2=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	arg2=(uint64_t)get_byte();
	register_index(arg2);
	regs[arg1]*=regs[arg2];
	return;
}
void DIV(){
	uint64_t arg1=0;
	uint64_t arg2=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	arg2=(uint64_t)get_byte();
	register_index(arg2);
	if(!regs[arg2]):
		die("0");
	else:
		regs[arg1]/=regs[arg2];
}
void XOR(){
	uint64_t arg1=0;
	uint64_t arg2=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	arg2=(uint64_t)get_byte();
	register_index(arg2);
	regs[arg1] ^= regs[arg2];
}
void JMP(uint8_t c){
	uint64_t arg1=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	if(arg1>=page)
		die("segfault");
	c-=17;
	switch(c)
	{
		case 0://jmp
			break;
		case 1://je
			if(!FLAG)
				break;
			return;
		case 2://jne
			if(FLAG)
				break;
			return;
		case 3://jg
			if(FLAG>0)
				break;
			return;
		case 4://jl
			if(FLAG<0)
				break;
			return
		default:
			return;
	}
	pc = arg1;
	return;
}
void DEC(){
	uint64_t arg1=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	regs[arg1]--;
}
void INC(){
	uint64_t arg1=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	regs[arg1]++;
}
void AND(){
	uint64_t arg1=0;
	uint64_t arg2=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	arg2=(uint64_t)get_byte();
	register_index(arg2);
	regs[arg1] &= regs[arg2];
	if(regs[arg1]==0)
		FLAG=0;
	else
		FLAG=1;
}
void OR(){
	uint64_t arg1=0;
	uint64_t arg2=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	arg2=(uint64_t)get_byte();
	register_index(arg2);
	regs[arg1] |= regs[arg2];
	if(regs[arg1]==0)
		FLAG=0;
	else
		FLAG=1;
}
void NOT(){
	uint64_t arg1=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);
	if(regs[arg1])
		regs[arg1]=0;
	else:
		regs[arg1]=1;
}
void MOV(){
	
}


void CALL()
{
	PUSH()
	register_index(arg1);
}
void do_push(){

}
void PUSH(uint8_t c){
	uint64_t arg1=0;
	arg1=(uint64_t)get_byte();
	register_index(arg1);

}
void run()
{
	uint8_t cmd=0;
	while(1){
		cmd=get_byte();
		switch(cmd){
			case 0:
				NOP();break;
			case 1:
			case 2:
			case 3:
			case 4:
			case 5:
				ADD(cmd);break;//1,2,4,8
			case 6:
			case 7:
			case 8:
			case 9:
			case 10:
				SUB(cmd);break;
			case 11:
				MUL();break;
			case 15:
				DIV();break;
			case 16:
				XOR();break;
			case 17:
			case 18:
			case 19:
			case 20:
			case 21:
				JMP();break;// jmp je jne jg jl
			case 22:
				OR();break;
			case 23:
				AND();break;
			case 24:
				NOT();break;
			case 25:
				INC();break;
			case 26:
				DEC();break;
	
			case 27:
				MOV();break;
			case 13:
				PUSH();break;
			case 14:
				POP();break;
			case 18:
				CALL();break;
			case 19:
				RET();break;
			case 23:
				IN();break;
			case 24:
				OUT();break;
			case 0xff:
				die("EXIT");
			default:
				die("unknow operation")
		}
	}
}
int main(){
	init();
	load();
	run();
}
