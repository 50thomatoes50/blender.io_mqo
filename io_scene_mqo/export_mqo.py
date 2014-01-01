# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
"""
This script exports a Metasequoia(*.mqo) files to Blender.

Usage:
Run this script from "File->Export" menu and then load the desired MQO file.

NO WIKI FOR THE MOMENT
http://wiki.blender.org/index.php/Scripts/Manual/Export/MQO


base source from : 
http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Multi-File_packages#Simple_obj_export
"""

import os
import time

import bpy
import mathutils
import bpy_extras.io_utils


def export_mqo(filepath, ob, rot90, scale):
    
        # Exit edit mode before exporting, so current object states are exported properly.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
        
    name = os.path.basename(filepath)
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, 'w')    
    print('Exporting %s' % realpath)
 
    if not ob or ob.type != 'MESH':
        raise NameError('Cannot export: active object %s is not a mesh.' % ob)
    me = ob.data
    fp.write("Metasequoia Document\nFormat Text Ver 1.0\n\nScene {\n	pos 0.0000 0.0000 1500.0000\n	lookat 0.0000 0.0000 0.0000\n	head -0.5236\n	pich 0.5236\n	bank 0.0000\n	ortho 0\n	zoom2 5.0000\n	amb 0.250 0.250 0.250\n	dirlights 1 {\n		light {\n			dir 0.408 0.408 0.816\n			color 1.000 1.000 1.000\n		}\n	}\n}\n")
   
   
   
    fp.write("Object \"%s\" {\n\tdepth 0\n\tfolding 0\n\tscale 1.000000 1.000000 1.000000\n\trotation 0.000000 0.000000 0.000000\n\ttranslation 0.000000 0.000000 0.000000\n\tvisible 15\n\tlocking 0\n\tshading 1\n\tfacet 59.5\n\tcolor 0.898 0.498 0.698\n\tcolor_type 0\n" % (me.name))

    fp.write("\tvertex %i {\n"% (len(me.vertices)))
    for v in me.vertices:
        x = scale*v.co
        #if rot90:
        #    fp.write("v %.5f %.5f %.5f\n" % (x[0], x[2], -x[1]))
        #else:
        fp.write("\t\t%.5f %.5f %.5f\n" % (x[0], x[1], x[2]))
    fp.write("\t}\n")
    
    
    
    fp.write("\tface %i {\n" % (len(me.edges)))
    for f in me.edges:
        fp.write("\t\t2 V(%i %i)\n" % (f.vertices[0], f.vertices[1]))
        
    fp.write("\t}\n")
    
    '''fp.write("\tface %i {\n" % (len(me.edges)+len(me.polygon)))
    if len(me.tessfaces_uv_textures) > 0:
        uvtex = me.tessfaces_uv_textures[0]
        for f in me.tessfaces_tessfaces:
            data = uvtex.data[f.index]
            fp.write("vt %.5f %.5f\n" % (data.uv1[0], data.uv1[1]))
            fp.write("vt %.5f %.5f\n" % (data.uv2[0], data.uv2[1]))
            fp.write("vt %.5f %.5f\n" % (data.uv3[0], data.uv3[1]))
            if len(f.vertices) == 4:
                fp.write("vt %.5f %.5f\n" % (data.uv4[0], data.uv4[1]))
 
        vt = 1
        for f in me.tessfaces:
            vs = f.vertices
            fp.write("f %d/%d %d/%d %d/%d" % (vs[0]+1, vt, vs[1]+1, vt+1, vs[2]+1, vt+2))
            vt += 3
            if len(f.vertices) == 4:
                fp.write(" %d/%d\n" % (vs[3]+1, vt))
                vt += 1        
            else:
                fp.write("\n")
    else:
        for f in me.tessfaces:
            vs = f.vertices
            fp.write("f %d %d %d" % (vs[0]+1, vs[1]+1, vs[2]+1))
            if len(f.vertices) == 4:
                fp.write(" %d\n" % (vs[3]+1))
            else:
                fp.write("\n")
    fp.write("\t}\n")
    '''

    fp.write("}\nEof\n")
    print('%s successfully exported' % realpath)
    fp.close()
    return