#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<stdint.h>
uint64_t page=0x1000;
uint8_t *code=0;
uint8_t *data=0;
uint64_t regs[0x10]={0};
uint64_t pc=0;
uint64_t msg=0;
uint64_t ins_ct=0x20;
regs[14]=0x800;//rbp
regs[15]=0x800;//rsp
int64_t FLAG=0;
uint8_t * ReadOnly=0;
void * PTR=0;

void segfault(uint64_t p, uint64_t move){
	if( p + move >=page && !(p<0x1000))
		die("segfault");
	return 1;
}
uint8_t get_byte(){
	uint8_t res=0;
	segfault(pc,1);
	res=code[pc++];
	return res;
}
uint64_t get_regs_idx(){
	uint64_t res=(uint64_t)get_byte();
	register_index(res);
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
void die(char *s){
	printf("%s\n",s);
	exit(1);
}
void init(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	void *buf=0;
	int f=open("/dev/urandom",O_RDONLY);
	if(f<=0)
		die("init");
	read(f,&buf,8);
	buf = (long unsigned int)buf & 0xfffffffffffff000;
	mmap((void *)buf,0x3000,3,0x22,0,0);
	close(f);
	code 	= 	buf;
	data 	= 	code + page;
	ReadOnly =  data + page;
}
void load(){
	int f = open("./game",O_RDONLY);
	uint64_t p1 = read(f,code,0x1000);
	uint64_t p2 = read(f,ReadOnly,0x1000);
	if( p1 != 0x1000 || p2 !=0x1000)
		die("load");
	close(f);
}
void NOP(){
	return;
}
void ADD(uint8_t c){
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=0;
	c-=1;
	switch(c)
	{
		case 0://reg + reg
			arg2=get_regs_idx();
			regs[arg1]+=regs[arg2];
			break;
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
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=0;
	c-=6;
	switch(c)
	{	
		case 0://reg - reg
			arg2=get_regs_idx();
			regs[arg1]-=regs[arg2];
			setflag(regs[arg1],regs[arg2]);
			break;
		case 1://reg - 1 byte
			arg2=(uint64_t)get_byte();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2);
			break;
		case 2://reg - 2 bytes
			arg2=(uint64_t)get_word();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2);
			break;
		case 3://reg - 4 bytes
			arg2=(uint64_t)get_dword();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2);
			break;
		case 4://reg - 4 bytes
			arg2=get_qword();
			regs[arg1]-=arg2;
			setflag(regs[arg1],arg2);
			break;
	}
}
void MUL(){
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=get_regs_idx();
	regs[arg1]*=regs[arg2];
	return;
}
void DIV(){
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=get_regs_idx();
	if(!regs[arg2])
		die("0");
	else
		regs[arg1]/=regs[arg2];
}
void XOR(){
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=get_regs_idx();
	regs[arg1] ^= regs[arg2];
}
void JMP(uint8_t c){
	uint64_t arg1=0;
	uint16_t * tmp=get_word();
	arg1=(uint64_t)*tmp;
	segfault(pc,arg1);
	c-=17;
	switch(c)
	{
		case 0:
			break;
		case 1://jz
			if(!FLAG)
				break;
			return;
		case 2:
			if(FLAG)
				break;
			return;
		case 3:
			if(FLAG>0)
				break;
			return;
		case 4:
			if(FLAG<0)
				break;
			return;
		default:
			return;
	}
	pc += arg1;
	return;
}
void DEC(){
	uint64_t arg1=get_regs_idx();
	regs[arg1]--;
}
void INC(){
	uint64_t arg1=get_regs_idx();
	regs[arg1]++;
}
void AND(){
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=get_regs_idx();
	regs[arg1] &= regs[arg2];
	if(regs[arg1]==0)
		FLAG=0;
	else
		FLAG=1;
}
void OR(){
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=get_regs_idx();
	regs[arg1] |= regs[arg2];
	if(regs[arg1]==0)
		FLAG=0;
	else
		FLAG=1;
}
void NOT(){
	uint64_t arg1=get_regs_idx();
	if(regs[arg1])
		regs[arg1]=0;
	else
		regs[arg1]=1;
}
void MOV(uint8_t c){
	c-=27;
	uint64_t arg1=get_regs_idx();
	uint64_t arg2=0;
	switch(c)
	{
		case 0://reg reg
			arg2=get_regs_idx();
			regs[arg1]=regs[arg2];
			break;
		case 1:
			arg2=(uint64_t)get_byte();
			regs[arg1]=arg2;
			break;
		case 2:
			arg2=(uint64_t)get_word();
			regs[arg1]=arg2;
			break;
		case 3:
			arg2=(uint64_t)get_dword();
			regs[arg1]=arg2;
			break;
		case 4:
			arg2=(uint64_t)get_qword();
			regs[arg1]=arg2;
			break;
		case 5://reg byte ptr
			arg2=(uint64_t)get_byte();
			segfault(arg2,1);
			regs[arg1] =* (uint8_t *)(arg2+data);
			break;
		case 6://reg byte ptr
			arg2=(uint64_t)get_word();
			segfault(arg2,2);
			regs[arg1] = * (uint16_t *)(arg2+data);
			break;
		case 7://reg byte ptr
			arg2=(uint64_t)get_dword();
			segfault(arg2,4);
			regs[arg1] = * (uint32_t *)(arg2+data);
			break;
		case 8://reg byte ptr ; mov rax,[addr]
			arg2=(uint64_t)get_qword();
			segfault(arg2,8);
			regs[arg1] = * (uint64_t *)(arg2+data);
			break;
	}

}
void do_push(uint64_t data){
	segfault(regs[15],-8);
	*(data+regs[15]) = data; 
	regs[15]-=8;
}
void PUSH(){
	uint64_t arg1=get_regs_idx();
	do_push(regs[arg1]);
}
uint64_t do_pop(){
	segfault(regs[15],8);
	uint64_t res = *(uint64_t *)data[regs[15]];
	regs[15] += 8;
	return res;
}
void POP(){
	uint64_t arg1=get_regs_idx();
	regs[arg1] = do_pop();
}
void CALL(uint8_t c){
	c-=38;
	uint64_t arg1=0;
	if(c){
		arg1=get_regs_idx();
		do_push(pc);
		pc = regs[arg1];
	}
	else{
		arg1=get_qword();
		do_push(pc);
		pc = arg1;
	}
}
void RET(){
	pc = do_pop();
}
uint64_t readint()
{
 char buf[0x10]={0};
 unsigned t=0;
 while(t<0x10-1)
 {
 	unsigned int res = read(0,&buf[t],1);
 	if(res!=1)
 		break;
 	if(buf[t]=='\n')
 	{
 		buf[t]=0;
 		break;
 	}
 	 t++;
 }
 return (uint64_t)strtol(buf,0,10);
}
void IN(uint8_t c){
	c-=41;
	uint8_t arg1;
	uint64_t num=0;
	switch(c){
		case 0:// read reg
			arg1= get_regs_idx();
			read(0,&regs[arg1],1);
			break;
		case 1:
			arg1= get_regs_idx();
			num = readint();
			regs[arg1]= num;
			break;
		case 2:
			num = regs[0x5];
			len = regs[0x4];
			segfault(num,len);
			read(0,data+num,len);
			break;
	}
}
void OUT(uint8_t c){
	c-=44;
	uint64_t arg1=0;
	switch(c){
		case 0:
			arg1 = regs[0x5];
			segfault(arg1,1);
			write(1,data[arg1],1);
			break;
		case 1:// for write RO data.
			arg1 = regs[0x5];
			segfault(arg1,1);
			printf("%s\n",ReadOnly[arg1]);
			break;
		case 2:
			arg1 = get_byte();
			segfault(arg1,1);
			write(1,data[arg1],1);
			break;
		case 3:
			arg1 = get_regs_idx();
			write(1,regs[arg1],8);
			break;
	}
}
void STORE(uint8_t c){
	c-=48;
	uint64_t arg1;
	uint64_t arg2;
	
	switch(c){ 
		case 0: //mov [rax],num
		    arg1 = get_regs_idx();
			arg2 = get_byte();
			segfault(regs[arg1],1);
			data[regs[arg1]] = regs[arg2];
			break;
		case 1:// not finished
		    arg1 = get_regs_idx();
		    arg2 = get_regs_idx();
			segfault(regs[arg1],8);
			memcpy(data[regs[arg1]],regs[arg2],8);
			break;
		case 2:
		    arg1 = get_regs_idx();
		    arg2 = get_dword();
			segfault(regs[arg1],4);
			memcpy(data[regs[arg1]],arg2,4);
			break;
		case 3:
			break;
	}
}
void LOAD(uint8_t c)
{
	c-=52;//0x34
	uint64_t arg1 = get_regs_idx();
	uint64_t arg2 = get_regs_idx();
	memset(regs[arg1],0,8);//warning
	switch(c){
		case 0:
			segfault(regs[arg2],regs[arg2]+1);
			memcpy(regs[arg1],data[regs[arg2]],1);
			break;
		case 1:
			segfault(regs[arg2],regs[arg2]+2);
			memcpy(regs[arg1],data[regs[arg2]],2);
			break;
		case 2:
			segfault(regs[arg2],regs[arg2]+4);
			memcpy(regs[arg1],data[regs[arg2]],4);
			break;
		case 3:
			segfault(regs[arg2],regs[arg2]+8);
			memcpy(regs[arg1],data[regs[arg2]],8);
			break;
			
	}
}
void Test()
{
	uint64_t arg1 = get_regs_idx();
	if(regs[arg1]==0)
		FLAG=1;
	else:
		FLAG=0;
}
void play()
{
	uint64_t arg1 = regs[4];
	ptr=malloc(arg1);
	puts("Content:");
	read(0,ptr,arg1);
}
void do_free()
{
	if(ptr)
	free(ptr);
	ptr=0;
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
				JMP(cmd);break;// jmp je jne jg jl
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
			case 28:
			case 29:
			case 30:
			case 31:
			case 32:
			case 33:
			case 34:
			case 35:
				MOV(cmd);break;
			case 36:
				PUSH();break;
			case 37:
				POP();break;
			case 38:
			case 39:
				CALL(cmd);break;
			case 40:
				RET();break;
			case 41:
			case 42:
			case 43:
				IN(cmd);break;
			case 44:
			case 45:
			case 46:
			case 47:
				OUT(cmd);break;
			case 48:
			case 49:
			case 50:
			case 51:
				STORE(cmd);break;
			case 52:
			case 53:
			case 54:
			case 55:
				LOAD(cmd);break;
			case 56:
				Test();break;
			case 57:
				play();
			case 58:
				do_free();
			case 0xff:
				die("EXT");
			default:
				die("OP");
		}
	}
}
int main(){
	init();
	load();
	run();
}
