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

# Script copyright (C) Thomas PORTASSAU (50thomatoes50)
# Contributors: Campbell Barton, Jiri Hnidek, Paolo Ciccone, Thomas Larsson, http://blender.stackexchange.com/users/185/adhi
#http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Multi-File_packages#Simple_obj_importer_and_exporter

"""
This script imports a Metasequoia(*.mqo) files to Blender.

Usage:
Run this script from "File->Import" menu and then load the desired MQO file.

NO WIKI FOR THE MOMENT
http://wiki.blender.org/index.php/Scripts/Manual/Import/MQO


base source from :
http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Multi-File_packages#Simple_obj_import
"""

import bpy
import os
import math
import mathutils
import re
import struct
import logging

def dprint(string, debug=False):
    if debug:
       logging.debug(string)
    return


def import_mqo(op, filepath, rot90, scale, debug):
    name = os.path.basename(filepath)
    realpath = os.path.realpath(os.path.expanduser(filepath))
    logging.basicConfig(filename=os.path.dirname(realpath)+os.sep+'import_mqo.log', level=logging.DEBUG)

    with open(realpath, 'rb') as fp:    # Universal read
        dprint('Importing %s' % realpath, debug)
        e = mathutils.Euler();
        e.rotate_axis('X', math.radians(90))
        m = e.to_matrix()
        verts = []
        faces = []
        edges = []
        texverts = []
        texfaces = []
        obj = False
        mat = False
        mat_nb = 0
        mat_list = []
        v = False
        vb = False
        v_nb = 0
        obj_name = ""
        f = False
        f_nb = 0
        f_index = 0
        f_mat = {}
        f_uv = {}

        for lineBin in fp:
            line = lineBin.decode('ascii')
            words = line.split()
            if len(words) == 0:                     ##Nothing
                pass
            elif words[0] == "}":                       ##end of mat or obj
                dprint('end something %d'% (fp.tell()), debug)
                if obj:                             ##if end of obj import it in blender
                    if v:
                        v=False
                        dprint('end of vertex %d'% (fp.tell()), debug)
                    elif vb:
                        vb=False
                        dprint('end of Bvertex', debug)
                    elif f:
                        f=False
                        dprint('end of face', debug)
                    else:
                        dprint('end of obj. importing :"%s"  %d' % (obj_name, fp.tell()), debug)
                        me = bpy.data.meshes.new(obj_name)
                        me.from_pydata(verts, [], faces)
                        me.update()
                        for mat_tmp in mat_list:
                            me.materials.append(mat_tmp)

                        if len(f_mat):
                            for fmk in f_mat.keys():
                                me.polygons[fmk].material_index = f_mat[fmk]

                        if len(f_uv):
                            uvtexture = me.uv_textures.new()
                            uvtexture.name = "MainUV"

                            uvlayer = me.uv_layers[-1]

                            start = 0
                            for i in range(len(faces)):
                                if i in f_uv.keys():
                                    for j in range(len(faces[i])):
                                        uvlayer.data[ start + j ].uv = (f_uv[i][ j*2 ], -f_uv[i][j*2+1] +1 )

                                start += len(faces[i])

                        scn = bpy.context.scene
                        ob = bpy.data.objects.new(obj_name, me)
                        scn.objects.link(ob)
                        scn.objects.active = ob
                        obj = False
                        v = False
                        v_nb = 0
                        obj_name = ""
                        f = False
                        f_nb = 0
                        f_index = 0
                        f_mat = {}
                        f_uv = {}
                        verts = []
                        faces = []
                        texverts = []
                        texfaces = []
                if mat:                             ##if end of mat import later in obj
                    dprint('end of mat', debug)
                    mat = False

            elif words[0] == 'Object':              ##detect an object
                dprint('begin of obj :%s' % words[1], debug)
                obj = True
                obj_name = words[1].strip('"')
            elif words[0] == 'Material':            ##detect materials
                dprint('begin of mat', debug)
                mat = True
                mat_nb = int(words[1].strip('"'))
            elif obj and words[0] == "vertex":      ##detect vertex when obj
                dprint('begin of ver', debug)
                v = True
                v_nb = int(words[1])
            elif obj and v and v_nb != 0:           ##get vertex coor when vertex and obj
                dprint('found a vertex', debug)
                (x,y,z) = (float(words[0]), float(words[1]), float(words[2]))
                if rot90:
                    V = mathutils.Vector((x,y,z))
                    vv = m*V
                    verts.append( (scale*vv.x, scale*vv.y, scale*vv.z) )
                else:
                    verts.append( (scale*x, scale*y, scale*z) )
                v_nb = v_nb -1
                if v_nb == 0:
                    #v = False
                    dprint('end of vertex? %d'% (fp.tell()), debug)
            elif obj and words[0] == "BVertex":
                vb = True
                v_nb = int(words[1])
                v_bytes = int(fp.readline().decode("ascii").split()[-1].strip("[]"))
                #dprint('nl=%s' % fp.readline(), debug)
                for i in range(v_nb):
                    tmp = struct.unpack("<fff", fp.read(4*3))
                    dprint('tmp = %s' % str(tmp), debug)
                    if rot90:
                        V = mathutils.Vector(tmp)
                        vv = m*V
                        verts.append( (scale*vv.x, scale*vv.y, scale*vv.z) )
                    else:
                        verts.append( (scale*tmp[0], scale*tmp[1], scale*tmp[2]) )
                    v_nb = v_nb -1
                    if v_nb == 0:
                        #v = False
                        dprint('end of vertex?', debug)

            elif obj and words[0] == "face":        ##detect face when obj
                dprint('begin of face', debug)
                f = True
                f_nb = int(words[1])
            elif obj and f and f_nb != 0:           ##get face vertex
                dprint('found a face', debug)
                f_vert_nb = int(words[0])
                if f_vert_nb == 2:
                    edges.append((int(words[1].strip('V(')), int(words[2].strip(')'))))
                elif f_vert_nb == 3:
                    faces.append((int(words[1].strip('V(')), int(words[3].strip(')')), int(words[2])))
                elif f_vert_nb == 4:
                    faces.append((int(words[1].strip('V(')), int(words[4].strip(')')), int(words[3]), int(words[2])))
                else:
                    dprint('error : face with %i vertex' % (f_vert_nb), debug)

                if "M(" in line:
                    for w in words:
                        if w.startswith("M("):
                            f_mat[f_index] = int(w.strip("M()"))

                if "UV(" in line:
                    for i in range(len(words)):
                        if words[i].startswith("UV("):
                            if f_vert_nb == 2:
                                f_uv[f_index] = [ float( words[i].strip("UV(")), float(words[i+1]), float(words[i+2]), float( words[i+3].strip(")"))  ]
                            elif f_vert_nb == 3:
                                f_uv[f_index] = [ float( words[i].strip("UV(")), float(words[i+1]), float(words[i+4]), float( words[i+5].strip(")")), float(words[i+2]), float(words[i+3])  ]
                            elif f_vert_nb == 4:
                                f_uv[f_index] = [ float( words[i].strip("UV(")), float(words[i+1]), float(words[i+6]), float( words[i+7].strip(")")), float(words[i+4]), float(words[i+5]), float(words[i+2]), float(words[i+3])  ]
                            else:
                                dprint('error : face UV with %i vertex' %(f_vert_nb), debug)

                f_index +=1
                f_nb = f_nb -1
                if f_nb ==0:
                    #f= False
                    dprint('end of face?', debug)
            elif mat and mat_nb > 0 :
                mat_tmp = bpy.data.materials.new(words[0].strip('"'))
                col_rgba = [1,1,1,1]
                colm = re.search(r"col\(([0-9. ]*)\)", line)
                if colm:
                    colm = colm.group().split()
                    for i in range(4):
                        col_rgba[i] = float(colm[i].strip('col()'))
                mat_tmp.diffuse_color = (col_rgba[0], col_rgba[1], col_rgba[2])
                if col_rgba[3] < 1.0:
                    mat_tmp.use_transparency = True
                    mat_tmp.alpha = col_rgba[2]

                for w in words:
                    if w.startswith("dif("):
                        mat_tmp.diffuse_intensity = float(w.strip('dif()'))
                    elif w.startswith("amb("):
                        mat_tmp.ambient = float(w.strip('amb()'))
                    elif w.startswith("emi("):
                        mat_tmp.emit = float(w.strip('emi()'))
                    elif w.startswith("spc("):
                        mat_tmp.specular_intensity = float(w.strip('spc()'))
                    elif w.startswith("power("):
                        mat_tmp.specular_intensity = float(w.strip('power()'))

                mat_list.append(mat_tmp)

                if "tex(" in line:
                    tex_filename = ""
                    for w in words:
                        if w.startswith("tex("):
                            tex_filename = w[5 : -2]
                            break

                    bltex = bpy.data.textures.new( tex_filename , "IMAGE")
                    bltex.__class__ = bpy.types.ImageTexture

                    if os.path.isfile(tex_filename):
                        #direct ie: C:\data .....
                        bltex.image = bpy.data.images.load(tex_filename)
                    elif os.path.isfile(os.path.dirname(filepath) + os.path.sep + tex_filename):
                        imgfile = os.path.dirname(filepath) + os.path.sep + tex_filename
                        bltex.image = bpy.data.images.load(imgfile)
                    elif os.path.isfile(os.path.dirname(filepath) + os.path.sep + "Texture"+ os.path.sep + tex_filename):
                        bltex.image = bpy.data.images.load(os.path.dirname(filepath) + os.path.sep + "Texture"+ os.path.sep + tex_filename)
                    else:
                        print("Can't find Texture file = %s"%(tex_filename))
                        print(tex_filename+" = ",os.path.isfile(tex_filename))
                        print(os.path.dirname(realpath) + os.path.sep + tex_filename+" = ",os.path.isfile(os.path.dirname(filepath) + os.path.sep + tex_filename))
                        print(os.path.dirname(filepath) + os.path.sep + "Texture"+ os.path.sep + tex_filename+" = ",os.path.isfile(os.path.dirname(filepath) + os.path.sep + "Texture"+ os.path.sep + tex_filename))

                    bltexslot = mat_tmp.texture_slots.create(0)
                    bltexslot.texture_coords = "UV"
                    bltexslot.texture = bltex

                if "aplane(" in line:
                    texa_filename = ""
                    for w in words:
                        if w.startswith("aplane("):
                            texa_filename = w[8:-2]
                            break

                    bltex = bpy.data.textures.new( texa_filename , "IMAGE")
                    bltex.__class__ = bpy.types.ImageTexture

                    if os.path.isfile(texa_filename):
                        #direct ie: C:\data .....
                        bltex.image = bpy.data.images.load(texa_filename)
                    elif os.path.isfile(os.path.dirname(filepath) + os.path.sep + texa_filename):
                        imgfile = os.path.dirname(filepath) + os.path.sep + texa_filename
                        bltex.image = bpy.data.images.load(imgfile)
                    elif os.path.isfile(os.path.dirname(filepath) + os.path.sep + "Alpha" + os.path.sep + texa_filename):
                        bltex.image = bpy.data.images.load(os.path.dirname(filepath) + os.path.sep + "Alpha"+ os.path.sep + texa_filename)
                    else:
                        print("Can't find Alpha Texture file = %s"%(texa_filename))
                        print(texa_filename+" = ",os.path.isfile(texa_filename))
                        print(os.path.dirname(realpath) + os.path.sep + texa_filename+" = ",os.path.isfile(os.path.dirname(filepath) + os.path.sep + texa_filename))
                        print(os.path.dirname(filepath) + os.path.sep + "Alpha" + os.path.sep + texa_filename+" = ",os.path.isfile(os.path.dirname(filepath) + os.path.sep + "Alpha" + os.path.sep + texa_filename))

                    bltexslot = mat_tmp.texture_slots.create(1)
                    bltexslot.use_map_color_diffuse = False
                    bltexslot.use_map_alpha = True
                    bltexslot.texture_coords = "UV"
                    bltexslot.texture = bltex

                if "bump(" in line:
                    texb_filename = ""
                    for w in words:
                        if w.startswith("bump("):
                            texb_filename = w[ 6 : -2]
                            break

                    bltex = bpy.data.textures.new( texb_filename , "IMAGE")
                    bltex.__class__ = bpy.types.ImageTexture

                    if os.path.isfile(texb_filename):
                        #direct ie: C:\data .....
                        bltex.image = bpy.data.images.load(texb_filename)
                    elif os.path.isfile(os.path.dirname(filepath) + os.path.sep + texb_filename):
                        imgfile = os.path.dirname(filepath) + os.path.sep + texb_filename
                        bltex.image = bpy.data.images.load(imgfile)
                    elif os.path.isfile(os.path.dirname(filepath) + os.path.sep + "Bump"+ os.path.sep + texb_filename):
                        bltex.image = bpy.data.images.load(os.path.dirname(filepath) + os.path.sep + "Bump"+ os.path.sep + texb_filename)
                    else:
                        print("Can't find bump Texture file = %s"%(texb_filename))
                        print(texb_filename+" = ",os.path.isfile(texb_filename))
                        print(os.path.dirname(realpath) + os.path.sep + texb_filename+" = ",os.path.isfile(os.path.dirname(filepath) + os.path.sep + texb_filename))
                        print(os.path.dirname(filepath) + os.path.sep + "Bump"+ os.path.sep + texb_filename+" = ",os.path.isfile(os.path.dirname(filepath) + os.path.sep + "Bump"+ os.path.sep + texb_filename))

                    bltexslot = mat_tmp.texture_slots.create(2)
                    bltexslot.use_map_color_diffuse = False
                    bltexslot.use_map_normal = True
                    bltexslot.texture_coords = "UV"
                    bltexslot.texture = bltex

                mat_nb -=1
                if mat_nb ==0:
                    #f= False
                    dprint('end of mat?', debug)
            else:
                dprint('don\'t know what is it', debug)
                pass

        msg = ".mqo import: Import finished"
        print(msg, "\n")
        op.report({'INFO'}, msg)
    return
