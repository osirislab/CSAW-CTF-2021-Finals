#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

#define PASSWORDLENGTH 32
#define TRUE 1
#define FALSE 0
#define BINARYNAME "level_one"

#define CONTENTLENGTH 200

char* password = "c43277249e73244ed4ec051363fac62d";
char* shell = "/bin/sh";

int foo1(void) {
	asm volatile(
		"pop %rdx\n"
		"ret\n"
	);
}

int foo2(void) {
	asm volatile(
		"inc %rax\n"
		"ret\n"
	);
}

int foo3(void) {
	asm volatile(
		"xor %rax, %rax\n"
		"ret\n"
	);
}

int foo4(void) {
	asm volatile(
		"pop %rdi\n"
		"ret\n"
	);
}

int foo5(void) {
	asm volatile(
		"movq %rax, (%rdx)\n"
		"ret\n"
	);
}

int foo6(void) {
	asm volatile(
		"pop %rax\n"
		"ret\n"
	);
}

int foo7(void) {
	asm volatile(
		"pop %rsi\n"
		"ret\n"
	);
}

int foo8(void) {
	asm volatile(
		"movl $0xf, %eax\n"
		"ret\n"
	);
}

int foo9(void) {
	asm volatile(
		"int $0x80\n"
		"ret\n"
	);
}

int foo10(void) {
	asm volatile(
		"syscall\n"
		"ret\n"
	);
}

void printBinary(){
    char c;
    FILE * f;
    f = fopen(BINARYNAME, "r");
    if(f == NULL){
        puts("Error reading hex of binary");
        exit(0);
    }
    c = fgetc(f);
    while (c != EOF){
        printf("%c", c);
        c = fgetc(f);
    }
    fclose(f);
    return;
}

char equalArrays(char a[], char b[], int size){
    for(int i = 0; i < size; i++){
        if(a[i]!=b[i]){
            return FALSE;
        }
    }
    return TRUE;
}

int password_is_correct(char* user_input){
    return equalArrays(password, user_input, PASSWORDLENGTH-1);
}

int runChallenge()
{
	char s;
	gets(&s);
	return 0;
}

int main(int argc, const char **argv, const char **envp)
{
	
	puts("Welcome to the AEG challenges!");
    char user_input[PASSWORDLENGTH];
    puts("Input password to continue:");
    printf("> ");
    fflush(stdout);
    fgets(user_input, PASSWORDLENGTH+2, stdin);
    if (password_is_correct(user_input)){
        puts("Correct password! :)");
        //puts("Here is the binary that is currently running on this box: ");
        //puts("-------------------------------------------------------------------");
        //printBinary();
        //puts("-------------------------------------------------------------------");
        puts("\nProceeding to the challenge...\n");
        fflush(stdout);
	printf("Main is at %x\n", **(main));
        runChallenge();
    }else{
        printf("Incorrect password. :(\n");
    }
    return 0;
}
