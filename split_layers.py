#!/usr/bin/python3

import sys
import os
import gdspy

orig_box_width=10.
orig_box_spacing=10.

layer_mapping = {
	'pwell' : [41],
	'nwell' : [42],
	'isolation' : [41,42],
	'gate' : [46],
	'nimplant' : [45],
	'pimplant' : [44],
	'contact' : [47,48],
	'metal1' : [49],
}

layout_path='Layout/magic'

#cellname='L500_MOSFET_aligning'
cellname='T10_RO51_NAND3'

magic_script="\n"
magic_script+="drc off"
magic_script+="\n"
magic_script+="box 0 0 0 0"
magic_script+="\n"
magic_script+="tech load scmos"
magic_script+="\n"
magic_script+="load "+layout_path+"/"+cellname+".mag"
magic_script+="\n"
magic_script+="drc off"
magic_script+="\n"
magic_script+="gds readonly true"
magic_script+="\n"
magic_script+="gds rescale false"
magic_script+="\n"
magic_script+="load "+cellname
magic_script+="\n"
magic_script+="gds flatten yes"
magic_script+="\n"
magic_script+="gds label no"
magic_script+="\n"
magic_script+="gds merge yes"
magic_script+="\n"
magic_script+="gds write gds/"+cellname
magic_script+="\n"
magic_script+="calma write gds/"+cellname
magic_script+="\n"
magic_script+="quit -noprompt"
magic_script+="\n"

print(os.popen("mkdir -p gds").read())
print(os.popen("magic -dnull -noconsole << EOF"+magic_script+"EOF").read())

gdsii=gdspy.GdsLibrary()
gdsii.read_gds(
	"gds/"+cellname+".gds",
)
cell=gdsii.extract(cellname)
cell=cell.flatten()
bb=cell.get_bounding_box()

p11=bb[0]-[orig_box_width,orig_box_width]-[orig_box_spacing,orig_box_spacing]
p12=bb[0]-[orig_box_spacing,orig_box_spacing]

p21=bb[1]+[orig_box_spacing,orig_box_spacing]
p22=bb[1]+[orig_box_spacing,orig_box_spacing]+[orig_box_width,orig_box_width]

cell=cell.flatten()

for layername in layer_mapping:
	ncell=cell.copy(layername,deep_copy=True)
	for idx in ncell.get_layers():
		if not idx in layer_mapping[layername]:
			ncell=ncell.remove_polygons(lambda pts, layer, datatype: layer == idx)
	ncell=ncell.add(gdspy.Rectangle(p11, p12, 1))
	ncell=ncell.add(gdspy.Rectangle(p21, p22, 1))
	ncell=ncell.flatten(single_layer=1,single_datatype=1)
	newgdsii=gdspy.GdsLibrary("mask_"+layername)
	newgdsii.add(ncell)
	newgdsii.write_gds("gds/mask_"+layername+".gds")

if len(sys.argv)==2:
	if sys.argv[1]=='-s':
		gdspy.LayoutViewer()
