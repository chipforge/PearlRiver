#!/usr/bin/python3
import gdspy
import numpy

darkfield_masks = [
	["nwell","pwell","pbase","nbase"],
	["fox","nimplant","pimplant","contact"],
	["via1","via2","glass"]
]

brightfield_masks = [
	["sti","sonos","gate","implant_stop"],
	["silicide_block","metal1","metal2","metal3"]
]

def get_offset(idx):
	x0=30000
	y0=30000
	x1=x0+34000
	y1=y0+34000

	if(idx==0):
		return [x0,y1]
	elif(idx==1):
		return [x1,y1]
	elif(idx==2):
		return [x0,y0]
	elif(idx==3):
		return [x1,y0]
	else:
		return [0,0]


def get_frame(bb):
	spacing=1000
	frame_width=200

	ret=[]
	p1=bb[0]
	p2=bb[1]

	pp1=[p1[0]-spacing,p1[1]-(spacing+frame_width)]
	pp2=[p1[0]-(spacing+frame_width),p2[1]+(spacing+frame_width)]
	stripe=gdspy.Rectangle(pp1, pp2, layer=1, datatype=0)
	ret.append(stripe)

	pp1=[p2[0]+spacing,p1[1]-(spacing+frame_width)]
	pp2=[p2[0]+(spacing+frame_width),p2[1]+(spacing+frame_width)]
	stripe=gdspy.Rectangle(pp1, pp2, layer=1, datatype=0)
	ret.append(stripe)

	pp1=[p1[0]-(spacing+frame_width),p2[1]+(spacing+frame_width)]
	pp2=[p2[0]+(spacing+frame_width),p2[1]+spacing]
	stripe=gdspy.Rectangle(pp1, pp2, layer=1, datatype=0)
	ret.append(stripe)

	pp1=[p1[0]-(spacing+frame_width),p1[1]-(spacing+frame_width)]
	pp2=[p2[0]+(spacing+frame_width),p1[1]-spacing]
	stripe=gdspy.Rectangle(pp1, pp2, layer=1, datatype=0)
	ret.append(stripe)

	return ret

def make_masks(frame,mask_type,mask_mappings):
	i=1
	for m in mask_mappings:
		outgdsii=gdspy.GdsLibrary(mask_type+str(i))

		gdsii=gdspy.GdsLibrary("top")
		gdsii.read_gds(frame, units='skip', rename={}, layers={}, datatypes={}, texttypes={})

		if(len(gdsii.top_level())==1):
			for c in gdsii.top_level():
				topcell=c.flatten(single_layer=1)
	
			#we have four tiles ready to be filled
			for idx in range(4):
				if(len(m)>idx):
					cellname="mask_"+m[idx]
					print("Adding "+cellname)
					ngdsii=gdspy.GdsLibrary(cellname)
					ngdsii.read_gds("Layout/gds/"+cellname+".gds", units='skip', rename={}, layers={}, datatypes={}, texttypes={})
					for c in ngdsii.top_level():
						cell=c.flatten(single_layer=1)
					try:
						pgs = cell.get_polygons()
					except:
						print("No polygons found")

					bb=cell.get_bounding_box()
					bb[0]=bb[0]+get_offset(idx)
					bb[1]=bb[1]+get_offset(idx)

					for stripe in get_frame(bb):
						topcell.add(stripe)

					for pg in pgs:
						pg=pg+get_offset(idx)
						if((idx>=0) and (idx<=3)):
							topcell.add(gdspy.Polygon(pg))

			topcell=topcell.flatten(single_layer=1)
			outgdsii.add(topcell)
			outgdsii.write_gds("Vendors/HKUST/Masks/"+mask_type+str(i)+".gds")
			i=i+1
		else:
			print("Error! Wrong about of top cells!")


make_masks("Vendors/HKUST/GDS/stepperMK_15mm_Dark.gds","darkfield",darkfield_masks)
make_masks("Vendors/HKUST/GDS/stepperMK_15mm_Bright.gds","brightfield",brightfield_masks)
