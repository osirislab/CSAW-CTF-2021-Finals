#include<stdio.h>
void ddd(char *s)
{
	for(unsigned int i =0;;i++)
	{
		if(s[i]==0)
			break;
		write(1,&s[i],1);
	}
}
int main()
{
 ddd("CCTV\n");
 //printf("")
}
