FROM python:3

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN pip3 install sympy numpy

WORKDIR /opt/chal

COPY server.py .
COPY flag.txt .
COPY cipher ./cipher
COPY private_key .
COPY public_key .
COPY random_poly .

RUN chmod 444 flag.txt && chmod 555 server.py && chmod -w .

USER nobody
CMD ["socat", "-T60", "TCP-LISTEN:5000,reuseaddr,fork","EXEC:python3 ./server.py"]
