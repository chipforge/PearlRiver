#!/usr/bin/python3

import gdspy
import os

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
magic_script+="gds write "+cellname
magic_script+="\n"
magic_script+="calma write "+cellname
magic_script+="\n"
magic_script+="quit -noprompt"
magic_script+="\n"

print(os.popen("magic -dnull -noconsole << EOF"+magic_script+"EOF").read())

gdsii=gdspy.GdsLibrary()
gdsii.read_gds(
	cellname+".gds",
	layers={
		41: 1,
		42: 1,
	}
)
cell=gdsii.extract(cellname)
cell=cell.flatten()
cell.remove_polygons(lambda pts, layer, datatype: layer != 1)
newgdsii=gdspy.GdsLibrary(name="top")
newgdsii.add(cell)
newgdsii.write_gds("test.gds")
#gdspy.LayoutViewer()
