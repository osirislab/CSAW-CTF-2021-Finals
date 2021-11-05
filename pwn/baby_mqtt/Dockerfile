# docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --rm -it -v $PWD:/whatever mqttdebug bash
FROM debian:stretch
RUN echo deb http://ftp.us.debian.org/debian/ stretch main > /etc/apt/sources.list
RUN echo deb http://archive.debian.org/debian wheezy-backports main >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y build-essential mlocate libc++-dev  g++-multilib g++

# Debug only
RUN apt-get install -y python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential tmux gdb vim
RUN python3 -m pip install --upgrade pwntools==4.5.1
RUN apt-get install -y locales
RUN locale-gen C.UTF-8
RUN locale -a
RUN update-locale LANG=C.UTF-8
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen
RUN apt-get install -y socat
