#!/usr/bin/python3

import sys
import os
import gdspy

orig_box_width=10.
orig_box_spacing=10.

layer_mapping = {
	'pwell' : [2],
	'nwell' : [3],
	'pbase' : [4],
	'nbase' : [5],
	'sti' : [6],
	'fox' : [7],
	'sonos' : [8],
	'gate' : [9],
	'implant_stop' : [10],
	'nimplant' : [11],
	'pimplant' : [12],
	'silicide_block' : [13],
	'contact' : [14],
	'metal1' : [15],
	'via1' : [16],
	'metal2' : [17],
	'via2' : [18],
	'metal3' : [19],
}

#layout_path='Layout'
layout_path='Library'

#cellname='L500_MOSFET_aligning'
#cellname='T10_RO51_NAND3'
#cellname='T6_INV'
#cellname='PearlRiver_die'
#cellname='L500_ZENER_W20_L1'
#cellname='L500_NPN_W34_L34_params'
#cellname='L500_PNP_W34_L34_params'
#cellname='L500_SONOS_PMOS_W3_L2_params'
#cellname='L500_SONOS_NMOS_W3_L2_params'
#cellname='L500_ZENER_W5_L2'
cellname='L500_ZENER_W5_L3'

magic_script="\n"
magic_script+="drc off"
magic_script+="\n"
magic_script+="box 0 0 0 0"
magic_script+="\n"
magic_script+="tech load scmos"
#magic_script+="tech load scmos-sub"
#magic_script+="tech load scmos-tm"
#magic_script+="tech load scmos-ls"
magic_script+="\n"
magic_script+="cif ostyle lambda=0.5(libresilicon)"
magic_script+="\n"
magic_script+="load "+layout_path+"/magic/"+cellname+".mag"
magic_script+="\n"
magic_script+="drc off"
magic_script+="\n"
magic_script+="gds readonly true"
magic_script+="\n"
magic_script+="gds rescale false"
magic_script+="\n"
magic_script+="gds label yes"
magic_script+="\n"
magic_script+="calma label yes"
magic_script+="\n"
magic_script+="load "+cellname
magic_script+="\n"
magic_script+="gds flatten yes"
magic_script+="\n"
magic_script+="gds merge yes"
magic_script+="\n"
magic_script+="gds write "+layout_path+"/gds/"+cellname
magic_script+="\n"
magic_script+="quit -noprompt"
magic_script+="\n"

print(os.popen("mkdir -p "+layout_path+"/gds").read())
print(os.popen("magic -dnull -noconsole << EOF"+magic_script+"EOF").read())

gdsii=gdspy.GdsLibrary()
gdsii.read_gds(layout_path+"/gds/"+cellname+".gds")
cell=gdsii.extract(cellname)
cell=cell.flatten()
bb=cell.get_bounding_box()

try:
	p11=bb[0]-[orig_box_width,orig_box_width]-[orig_box_spacing,orig_box_spacing]
	p12=bb[0]-[orig_box_spacing,orig_box_spacing]

	p21=bb[1]+[orig_box_spacing,orig_box_spacing]
	p22=bb[1]+[orig_box_spacing,orig_box_spacing]+[orig_box_width,orig_box_width]

	cell=cell.add(gdspy.Rectangle(p11, p12, 1))
	cell=cell.add(gdspy.Rectangle(p21, p22, 1))
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
		newgdsii.write_gds(layout_path+"/gds/mask_"+layername+".gds")

except:
	print("Can't do this")




if len(sys.argv)==2:
	if sys.argv[1]=='-s':
		gdspy.LayoutViewer()
