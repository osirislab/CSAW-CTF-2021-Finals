#FROM python:3 #doesn't install gmpy2 correctly
FROM ubuntu:20.04

RUN apt update && apt install -y vim python3-pip socat libgmp-dev libmpfr-dev libmpc-dev 

RUN pip3 install sympy numpy gmpy2

RUN useradd -ms /bin/bash chal

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /opt/chal

COPY server.py .
COPY flag.txt .
COPY password.txt .
COPY cipher ./cipher

RUN chown -R chal:chal /opt/chal 
RUN chown root:root flag.txt
RUN chmod 444 flag.txt password.txt && chmod 555 server.py
# && chmod -w .

#RUN USERADD -ms /bin/bash chal
USER chal
#USER nobody
CMD ["socat", "-T60", "TCP-LISTEN:5000,reuseaddr,fork","EXEC:python3 ./server.py"]
