# n132
def flush(data)
    with open("./game",'wb') as f:
        f.write(data.ljust(0x1000,b'\0'))
def Test(name):
    name()
def secure_check():
    res=b''
    res+=b''

if __name__ == "__main__":
    flush(Test(secure_check))