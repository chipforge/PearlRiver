#!/usr/bin/python3
import gdspy
import numpy

#spacing=1000
spacing=500
frame_width=200
square_middle=18750

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
	x0=20000
	y0=20500
	x1=95000
	y1=95500

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

def get_layer_location(idx,w,h):
	ret=get_offset(idx)
	#18750
	ret[0]=ret[0]-w/2
	ret[1]=ret[1]-h/2
	if(idx==0):
		ret[0]=ret[0]+square_middle
		ret[1]=ret[1]-square_middle
	elif(idx==1):
		ret[0]=ret[0]-square_middle
		ret[1]=ret[1]-square_middle
	elif(idx==2):
		ret[0]=ret[0]+square_middle
		ret[1]=ret[1]+square_middle
	elif(idx==3):
		ret[0]=ret[0]-square_middle
		ret[1]=ret[1]+square_middle

	return ret

def get_frame(bb):
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

def mirrored_polygons(cell):
	bb=cell.get_bounding_box()

	zeroing_offset=[0,0]
	zeroing_offset[0]=bb[0][0]
	zeroing_offset[1]=bb[0][1]

	width=bb[1][0]-bb[0][0]

	pgs=cell.get_polygons()

	for pg in pgs:
		for tp in pg:
			tp[0]=tp[0]-zeroing_offset[0]
			tp[1]=tp[1]-zeroing_offset[1]
			tp[0]=width-tp[0]

	return pgs

def make_masks(frame,mask_type,mask_mappings):
	i=1
	for m in mask_mappings:
		outgdsii=gdspy.GdsLibrary(mask_type+str(i))

		gdsii=gdspy.GdsLibrary("top")
		gdsii.read_gds(frame, units='skip', rename={}, layers={}, datatypes={}, texttypes={})

		topcell=gdspy.Cell("mask_"+mask_type+str(i))
		for c in gdsii.top_level():
			topcell.add(c.flatten(single_layer=1))
		topcell=topcell.flatten(single_layer=1)

		toppgs=topcell.get_polygons()
		#we have four tiles ready to be filled
		for idx in range(4):
			if(len(m)>idx):
				cellname="mask_"+m[idx]
				tp=get_offset(idx)
				fs=2000
				tp[1]=97800
				if((idx==2)or(idx==3)):
					tp[1]=16000
				if((idx==1)or(idx==3)):
					tp[0]=tp[0]-(75000/2)

				text=gdspy.Text(cellname, fs, tp)
				toppgs=gdspy.fast_boolean(toppgs,text,"xor", precision=0.001, max_points=800, layer=0)
		topcell=gdspy.Cell(mask_type+str(i))
		topcell.add(toppgs)

		for idx in range(4):
			if(len(m)>idx):
				cellname="mask_"+m[idx]
				ngdsii=gdspy.GdsLibrary(cellname)
				ngdsii.read_gds("Layout/gds/"+cellname+".gds", units='skip', rename={}, layers={}, datatypes={}, texttypes={})
				cell=gdspy.Cell(cellname)
				for c in ngdsii.top_level():
					cell.add(c.flatten(single_layer=1))
				cell=cell.flatten(single_layer=1)
				pgs = mirrored_polygons(cell)

				bb=cell.get_bounding_box()
				zeroing_offset=[0,0]
				zeroing_offset[0]=bb[0][0]
				zeroing_offset[1]=bb[0][1]
				bb[0]=bb[0]-zeroing_offset
				bb[1]=bb[1]-zeroing_offset
				bb=bb*5

				w=bb[1][0]-bb[0][0]
				h=bb[1][1]-bb[0][1]
				offset=get_layer_location(idx,w,h)

				for pg in pgs:
					pg=pg*5
					pg=pg+offset
					topcell.add(gdspy.Polygon(pg))

				bb[0]=bb[0]+offset
				bb[1]=bb[1]+offset

				for stripe in get_frame(bb):
					topcell.add(stripe)

		topcell=topcell.flatten(single_layer=1)
		outgdsii.add(topcell)
		outgdsii.write_gds("Vendors/HKUST/Masks/"+mask_type+str(i)+".gds")
		i=i+1


make_masks("Vendors/HKUST/GDS/stepperMK_15mm_Dark.gds","darkfield",darkfield_masks)
make_masks("Vendors/HKUST/GDS/stepperMK_15mm_Bright.gds","brightfield",brightfield_masks)
