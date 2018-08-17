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

tw=2

x1=0
x2=100

for i in range(1,20):
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
