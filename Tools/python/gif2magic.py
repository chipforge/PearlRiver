#!/usr/bin/python3
from PIL import ImageSequence
from PIL import Image
im = Image.open("Images/apple_monochrome.png").convert("L")
#im.show()
bbox=im.getbbox()
data=list(im.getdata(0))
for y in range(0,bbox[3]):
	line=""
	for x in range(0,bbox[2]):
		if(data[x*y]==255):
			line+=" "
		elif(data[x*y]==0):
			line+="*"
		else:
			line+="+"
	print(line)

#for frame in ImageSequence.Iterator(im):
#	help(frame)
