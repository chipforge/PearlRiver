#!/usr/bin/python3
file = open("Library/magic/L500_RESISTOR_1k_M1.mag","w") 
file.write("magic")
file.write("\n")
file.write("tech scmos")
file.write("\n")
file.write("timestamp 1534321654")
file.write("\n")
file.write("<< metal1 >>")
file.write("\n")

num_stripes=100
R=1e3
tw=1
rho=2.65e-8 # Ohm * meter
h=600e-9 # 600 nm
lam=1e-6 # lambda = 1 um
A=h*lam*tw # in square meter
l=((A*R)/rho)/lam

x1=0
x2=round(l/num_stripes)

for i in range(1,num_stripes):
	rect="rect "
	rect+=str(x1)
	rect+=" "
	rect+=str(i*tw*2)
	rect+=" "
	rect+=str(x2)
	rect+=" "
	rect+=str(i*tw*2+tw)
	file.write(rect+"\n")
	rect="rect "
	rect+=str(x1) if((i%2)==0) else str(x2-tw)
	rect+=" "
	rect+=str(i*tw*2)
	rect+=" "
	rect+=str(x1+tw) if ((i%2)==0) else str(x2)
	rect+=" "
	rect+=str((i+1)*tw*2)
	file.write(rect+"\n")

file.write("<< end >>")
file.write("\n")
file.close()
