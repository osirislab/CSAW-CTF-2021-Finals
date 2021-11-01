#include<stdio.h>
unsigned int ct = 0;
void survey()
{
    char vul[56]={0};
    size_t reason_length=0x50;
    size_t length=0x3c;

    char comment[0x50]={0};
    size_t age;
    char *buf;
    char reason[0x50]={0};

REPEAT:

    printf("Who are you:\n");
    buf = malloc(length);
    read(0,buf,length);

    printf("How old are you:\n");
    scanf("%d",&age);

    printf("What's the name of movie?\n");
    read(0,reason,reason_length);

    printf("Any comments about the movie:\n");
    read(0,comment,length);

    ct++;
    
    printf("Name: %s\n",buf);
    printf("Age: %d\n", age);
    printf("Reason: %s\n", reason);
    printf("Comment: %s\n", comment);

    sprintf(vul, "%d comment so far. We will review them as soon as we can", ct);
    puts(vul);

    if ( ct > 299 )
    {
        puts("Thank you for your comments!");
        exit(0);
    }
    while ( 1 )
    {
        char choice[8]={0};
        printf("Would you like to leave another comment? <y/n>: ");
        read(0, &choice, 2);
        if ( choice[0] == 89 || choice[0] == 121 )
        {
            free(buf);
            goto REPEAT;
        }
        if ( choice[0] == 78 || choice[0] == 110 )
            break;
        puts("Wrong choice.");
    }
}
void init()
{
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
}
int main()
{
    init();
    puts("Spirited away opens the door of binary for me. Hope you guys enjoy this one.");
    survey();
}
