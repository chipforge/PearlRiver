#!/usr/bin/python3

import gdspy
import os

layer_mapping = {
	'pwell' : {
		41: 1,
	},
	'nwell' : {
		42: 1,
	}
}

cellname="L500_MOSFET_aligning"

magic_script="\n"
magic_script+="drc off"
magic_script+="\n"
magic_script+="box 0 0 0 0"
magic_script+="\n"
magic_script+="tech load scmos"
magic_script+="\n"
magic_script+="load Layout/magic/"+cellname+".mag"
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


for layername in layer_mapping:
	gdsii=gdspy.GdsLibrary(layername)
	gdsii.read_gds(
		"gds/"+cellname+".gds",
		layers=layer_mapping[layername],
		rename={cellname:layername},
	)
	#cell=gdsii.extract(layername)
	#cell.name=layername
	#cell=cell.flatten()
	#cell.remove_polygons(lambda pts, layer, datatype: layer != 1)
	#newgdsii=gdspy.GdsLibrary("mask_"+layername)
	#newgdsii.add(cell)
	#newgdsii.write_gds("gds/mask_"+layername+".gds")
