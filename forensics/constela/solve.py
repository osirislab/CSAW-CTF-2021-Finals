import pyshark
from base64 import *
import matplotlib.pyplot as plt

cap = pyshark.FileCapture('constela.pcapng')
data = []
c = -1

for i in range(6072):
	try:
		if cap[i]['DNS'].flags == '0x00008183': # these are the packets containing data
				value = str(cap[i]['DNS'].qry_name).replace('.com','').replace('.cable.rcn','')
				if c > -1:
					if value == data[c] or value == 'connectivity-check.ubuntu':
						continue
					else:
						data.append(value)
						#print(value)
						c += 1
				else:
					data.append(value)
					#print(value)
					c += 1
	except:
		continue

actual_data = []
for i in range(0,len(data),2):
	line = b64decode((data[i]+data[i+1]).encode('utf-8')).decode('utf-8')
	#print(line)
	actual_data.append(line)

x = []
y = []
z = []
for co in actual_data:
	arr = co.split(',')
	x.append(float(arr[2]))
	y.append(float(arr[4]))
	z.append(float(arr[9]))
	#print(x[-1],y[-1],z[-1])

# Creating image
plt.scatter(x,z,color = "green", marker="s",s = 140, alpha=1.)
plt.show()
