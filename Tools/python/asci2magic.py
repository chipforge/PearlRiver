#!/usr/bin/python3
import os
import sys

inar=[]
outar=[]

lc=0
with open("Images/apple.txt", "r") as ins:
	for line in ins:
		inar.append(line)
	ins.close()

for line in inar:
	cc=0
	for c in line:
		if(c=="*"):
			outar.append("rect "+str(cc)+" "+str(len(inar)-lc)+" "+str(cc+1)+" "+str(len(inar)-lc+1))
		cc+=1
	lc+=1

with open("Library/magic/KALLISTI.mag", "w") as out:
	out.write("magic\n")
	out.write("tech scmos\n")
	out.write("timestamp 1533657739\n")
	out.write("<< metal3 >>\n")
	for line in outar:
		out.write(line+"\n")
	out.write("<< end >>\n")
	out.close()
