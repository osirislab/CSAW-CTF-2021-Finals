
# generate_fmt_string_source_code.py
from random import shuffle, choice, seed

def generate_level_one_source_code(filename_stem, password, random_seed):
    seed(random_seed)
    file_content_part_one = f"""
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <unistd.h>
    #include <sys/mman.h>

    #define PASSWORDLENGTH 32
    #define TRUE 1
    #define FALSE 0
    #define BINARYNAME \"{filename_stem}.txt\"

    #define CONTENTLENGTH 150

    char* password = \"{password}\";
    char* shell = \"/bin/sh\";\n\n
    """
    #char* shell = '{bin_sh}';

    gadget_list = ["pop %rdx", "inc %rax", "xor %rax, %rax", "pop %rdi", "movq %rax, (%rdx)",
            "pop %rax", "pop %rsi", "movl $0xf, %eax", "int $0x80", "syscall"]
    function_list = f"""""";
    shuffle(gadget_list)
    
    i = 1
    for gadget in gadget_list:
        function_list += f"""
        void foo"""+str(i)+"""(){
        \tasm volatile(
        """
        function_list += f"""\t\t\"""" 
        function_list += gadget 
        function_list += f"""\\n\""""
        function_list += f"""
            \t\t"ret\\n"
        \t);
        }}\n
        """
        i += 1
    file_content_last_part = f"""
    char equalArrays(char a[], char b[], int size){{
        for(int i = 0; i < size; i++){{
            if(a[i]!=b[i]){{
                return FALSE;
            }}
        }}
        return TRUE;
    }}

    void printBinary(){{
        char c;
        FILE * f;
        f = fopen(BINARYNAME, "r");
        if(f == NULL){{
            puts("Error reading hex of binary");
            exit(0);
        }}
        c = fgetc(f);
        while (c != EOF){{
            printf("%c", c);
            c = fgetc(f);
        }}
        fclose(f);
        return;
    }}

    int password_is_correct(char* user_input){{
        return equalArrays(password, user_input, PASSWORDLENGTH-1);
    }}

    void runChallenge(){{
        char s;
        gets(&s);
        return 0;
    }}

    int main(int argc, char **argv){{
        puts(\"Welcome to the AEG challenges!\");
        char user_input[PASSWORDLENGTH];
        puts(\"Input password to continue:\");
        printf(\"> \");
        fflush(stdout);
        fgets(user_input, PASSWORDLENGTH+2, stdin);
        if (password_is_correct(user_input)){{
            puts(\"Correct password! :)\");
            puts(\"Here is the binary that is currently running on this box: \");
            puts(\"-------------------------------------------------------------------\");
            printBinary();
            puts(\"-------------------------------------------------------------------\");
            puts(\"\\nProceeding to the challenge...\\n\");
            printf(\"Main is at %lx\\n\", **(main));
            fflush(stdout);
            runChallenge();
        }}else{{
            printf(\"Incorrect password. :(\");
        }}
    }}
    """
    f = open(filename_stem+".c", "w")
    f.write(file_content_part_one)
    f.write(function_list)
    f.write(file_content_last_part)
    f.close()
    return


def generate_intermediate_Dockerfile(filename, round_number, port_base):
    print("In generate_intermediate_Dockerfile: port_base = " + str(port_base) + " and round_number = " + str(round_number))
    port = port_base+round_number
    file_content=f"""FROM debian:stretch

    RUN apt-get update && apt-get upgrade -y && dpkg --add-architecture i386 && apt-get update && apt-get install -y libc6-i386 socat file && rm -rf /var/lib/apt/lists/*

    RUN useradd -M chal

    WORKDIR /opt/chal

    COPY binary_{round_number} .
    COPY message.txt .
    COPY binary_{round_number}.txt .

    RUN chown -R root:chal /opt/chal && \
      chmod 444 /opt/chal/message.txt && \
      chmod 555 /opt/chal/binary_{round_number} && \
      chmod 444 /opt/chal/binary_{round_number}.txt

    EXPOSE 5000
    USER chal
    CMD ["socat", "-T60", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./binary_{round_number}"]
    """
    f = open(filename, "w")
    f.write(file_content)
    f.close()

def generate_intermediate_level_four_Dockerfile(filename, round_number, port_base):
    print("In generate_intermediate_Dockerfile: port_base = " + str(port_base) + " and round_number = " + str(round_number))
    port = port_base+round_number
    file_content=f"""FROM ubuntu:20.04

    RUN apt-get update && apt-get upgrade -y && dpkg --add-architecture i386 && apt-get update && apt-get install -y libc6-i386 socat file && rm -rf /var/lib/apt/lists/*

    RUN useradd -M chal

    WORKDIR /opt/chal

    COPY binary_{round_number} .
    COPY message.txt .
    COPY binary_{round_number}.txt .

    RUN chown -R root:chal /opt/chal && \
      chmod 444 /opt/chal/message.txt && \
      chmod 555 /opt/chal/binary_{round_number} && \
      chmod 444 /opt/chal/binary_{round_number}.txt

    EXPOSE 5000
    USER chal
    CMD ["socat", "-T60", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./binary_{round_number}"]
    """
    f = open(filename, "w")
    f.write(file_content)
    f.close()



def generate_final_Dockerfile(filename, round_number, port_base):
    port = port_base + round_number
    file_content=f"""FROM debian:stretch

    RUN apt-get update && apt-get upgrade -y && dpkg --add-architecture i386 && apt-get update && apt-get install -y libc6-i386 socat file && rm -rf /var/lib/apt/lists/*

    RUN useradd -M chal

    WORKDIR /opt/chal

    COPY binary_{round_number} .
    COPY binary_{round_number}.txt .
    COPY flag.txt .

    RUN chown -R root:chal /opt/chal && \
      chmod 444 /opt/chal/flag.txt && \
      chmod 555 /opt/chal/binary_{round_number} && \
      chmod 444 /opt/chal/binary_{round_number}.txt

    EXPOSE 5000
    USER chal
    CMD ["socat", "-T60", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./binary_{round_number}"]
    """
    f = open(filename, "w")
    f.write(file_content)
    f.close()

