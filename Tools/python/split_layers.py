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

def get_magic_script(layout_path,cellname):
	magic_script="\n"
	magic_script+="drc off"
	magic_script+="\n"
	magic_script+="box 0 0 0 0"
	magic_script+="\n"
	magic_script+="tech load scmos"
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
	return magic_script

if '-n' in sys.argv:
	if len(sys.argv) >= sys.argv.index('-n')+2:
		cellname=sys.argv[sys.argv.index('-n')+1]
		if '-l' in sys.argv:
			layout_path='Library'
		else:
			layout_path='Layout'

		print(os.popen("mkdir -p "+layout_path+"/gds").read())
		print(os.popen("magic -dnull -noconsole << EOF"+get_magic_script(layout_path,cellname)+"EOF").read())

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

			if '-s' in sys.argv:
				gdspy.LayoutViewer()

		except:
			print("Can't do this")
	else:
		print("No cell name given. Use -n!")
else:
	print("No cell name given. Use -n!")
