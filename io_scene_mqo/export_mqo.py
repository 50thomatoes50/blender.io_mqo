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

# Script copyright (C) Thomas PORTASSAU (50thomatoes50)
# Contributors: Campbell Barton, Jiri Hnidek, Paolo Ciccone, Thomas Larsson, http://blender.stackexchange.com/users/185/adhi

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
import pprint
import bpy
import mathutils
import bpy_extras.io_utils


def export_mqo(filepath, objects, rot90, invert, edge, uv_exp, uv_cor, mat_exp, scale):
    
        # Exit edit mode before exporting, so current object states are exported properly.
    #if bpy.ops.object.mode_set.poll():
    #    bpy.ops.object.mode_set(mode='OBJECT')
        
    name = os.path.basename(filepath)
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, 'w')
    fw = fp.write
    print('Exporting %s' % realpath)
     
    fw("Metasequoia Document\nFormat Text Ver 1.0\n\nScene {\n    pos 0.0000 0.0000 1500.0000\n    lookat 0.0000 0.0000 0.0000\n    head -0.5236\n    pich 0.5236\n    bank 0.0000\n    ortho 0\n    zoom2 5.0000\n    amb 0.250 0.250 0.250\n    dirlights 1 {\n        light {\n            dir 0.408 0.408 0.816\n            color 1.000 1.000 1.000\n        }\n    }\n}\n")
    
    '''if mat_exp:
        fw("Material  %d{\n" % (len(me.materials)))
        for mat in me.materials:
            fw("\t\"%s\" " % (mat.name))
            fw("col(%.3f %.3f %.3f %.3f)" % (mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], mat.alpha))
            fw(" dif(%.3f)" % (mat.diffuse_intensity))
            fw(" amb(%.3f)" % (mat.ambient))
            fw(" emi(%.3f)" % (mat.emit))
            fw(" spc(%.3f)" % (mat.emit))
            fw(" power(5)\n")
        fw("}\n")'''
    
    inte_mat = 0
    tmp_mat = []
    
    for ob in objects:
        if not ob or ob.type != 'MESH':
            print('Cannot export: active object %s is not a mesh.' % ob)
        else:
            me = ob.data
            inte_mat = exp_obj(fw, me, ob.rotation_euler, ob.location, rot90, invert, edge, uv_exp, uv_cor, ob.scale, mat_exp, inte_mat, tmp_mat)
    
    if mat_exp:        
        mat_fw(fw, tmp_mat)
    
    fw("\nEof\n")
    print('%s successfully exported' % realpath)
    fp.close()
    return
    
def exp_obj(fw, me, rotat, loca, rot90, invert, edge, uv_exp, uv_cor, scale, mat_exp, inte_mat, tmp_mat):
    
    pi = 3.141594
    #fw("Object \"%s\" {\n\tdepth 0\n\tfolding 0\n\tscale %.6f %.6f %.6f\n\trotation %.6f %.6f %.6f\n\ttranslation %.6f %.6f %.6f\n\tvisible 15\n\tlocking 0\n\tshading 1\n\tfacet 59.5\n\tcolor 0.898 0.498 0.698\n\tcolor_type 0\n" % (me.name, scale[0], scale[1], scale[2], 180*rotat.x/pi, 180*rotat.y/pi, 180*rotat.z/pi, loca[0], loca[1], loca[2]))
    fw("Object \"%s\" {\n\tdepth 0\n\tfolding 0\n\tscale 1.0 1.0 1.0\n\trotation 1.0 1.0 1.0\n\ttranslation 1.0 1.0 1.0\n\tvisible 15\n\tlocking 0\n\tshading 1\n\tfacet 59.5\n\tcolor 0.898 0.498 0.698\n\tcolor_type 0\n" % (me.name))
    print("Exporting obj=\"%s\" inte_mat=%i" %(me.name, inte_mat))
    inte_mat_obj = inte_mat
    if mat_exp:
        for mat in me.materials:
            inte_mat = mat_extract(mat, tmp_mat, inte_mat)
        
        
    fw("\tvertex %i {\n"% (len(me.vertices)))
    for v in me.vertices:
        if rot90:
            fw("\t\t%.5f %.5f %.5f\n" % (v.co[0], v.co[2], v.co[1]))
        else:
            fw("\t\t%.5f %.5f %.5f\n" % (v.co[0], v.co[1], v.co[2]))
    fw("\t}\n")
    
    me.update(False, True)
    faces = me.tessfaces
    lostEdges = 0
    for e in me.edges:
        if e.is_loose:
            lostEdges+=1
    if edge:
        fw("\tface %i {\n" % (len(faces)+lostEdges))
        for e in me.edges:
            if e.is_loose:
                fw("\t\t2 V(%i %i)\n" % (e.vertices[0], e.vertices[1]))
    else:
        fw("\tface %i {\n" % (len(faces)))
    
    me.update(False, True)     
    for f in faces:
        vs = f.vertices
        if len(f.vertices) == 3:
            if invert:
                fw("\t\t3 V(%d %d %d)" % (vs[0], vs[2], vs[1]))
            else:
                fw("\t\t3 V(%d %d %d)" % (vs[0], vs[1], vs[2]))
        if len(f.vertices) == 4:
            if invert:
                fw("\t\t4 V(%d %d %d %d)" % (vs[0], vs[3], vs[2], vs[1]))
            else:
                fw("\t\t4 V(%d %d %d %d)" % (vs[0], vs[1], vs[2], vs[3]))
                
        fw(" M(%d)" % (f.material_index+inte_mat_obj))
        
        try:
            data = me.tessface_uv_textures.active.data[f.index]
            if (uv_exp):
                if len(f.vertices) == 3:
                    if uv_cor:
                        fw(" UV(%.5f %.5f %.5f %.5f %.5f %.5f)" % (data.uv1[0], 1-data.uv1[1], data.uv3[0], 1-data.uv3[1], data.uv2[0], 1-data.uv2[1]))
                    else:
                        fw(" UV(%.5f %.5f %.5f %.5f %.5f %.5f)" % (data.uv1[0], data.uv1[1], data.uv2[0], data.uv2[1], data.uv3[0], data.uv3[1]))
                if len(f.vertices) == 4:
                    if uv_cor:
                        fw(" UV(%.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f)" % (data.uv1[0], 1-data.uv1[1], data.uv2[0], 1-data.uv2[1], data.uv3[0], 1-data.uv3[1], data.uv4[0], 1-data.uv4[1]))
                    else:
                        fw(" UV(%.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f)" % (data.uv1[0], data.uv1[1], data.uv2[0], data.uv2[1], data.uv3[0], data.uv3[1], data.uv4[0], data.uv4[1]))   
        except AttributeError:
            pass
        
        fw("\n")
    fw("\t}\n")

    fw("}\n")
    return inte_mat
    
    
def mat_extract(mat, tmp, index):
    #l = "\t\"" + mat.name + "\" " + "col(" + str(mat.diffuse_color[0]) + " " + str(mat.diffuse_color[1]) + " " + str(mat.diffuse_color[2]) + " " + str(mat.alpha) + ")" + " dif(" + str(mat.diffuse_intensity) + ")" + " amb(" + str(mat.ambient) + ")" + " emi(" + str(mat.emit) + ")" + " spc(" + str(mat.specular_intensity) + ")" + " power(5)\n"
    print("added mat:%s / index #%i" % (mat.name,index))
    l = "\t\"%s\" col(%.3f %.3f %.3f %.3f) dif(%.3f) amb(%.3f) emi(%.3f) spc(%.3f) power(5)\n" % (mat.name, mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], mat.alpha, mat.diffuse_intensity, mat.ambient, mat.emit, mat.specular_intensity)
    tmp.append(l)
    return index + 1
    
    
def mat_fw(fw, tmp):
    fw("Material  %d{\n" % (len(tmp)))
    for mat in tmp:
        fw("%s" % (mat))
        '''fw("\t\"%s\" " % (mat.name))
        fw("col(%.3f %.3f %.3f %.3f)" % (mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], mat.alpha))
        fw(" dif(%.3f)" % (mat.diffuse_intensity))
        fw(" amb(%.3f)" % (mat.ambient))
        fw(" emi(%.3f)" % (mat.emit))
        fw(" spc(%.3f)" % (mat.specular_intensity))
        fw(" power(5)\n")'''
    fw("}\n")
    