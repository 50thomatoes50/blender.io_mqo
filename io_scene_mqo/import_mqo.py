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

import bpy, os, math, mathutils

def dprint(string, debug=False):
    if debug:
        print("\t",string)
    return
    
    
def import_mqo(op, filepath, rot90, scale, debug):
    name = os.path.basename(filepath)
    realpath = os.path.realpath(os.path.expanduser(filepath))
    with open(realpath, 'rU') as fp:    # Universal read
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
        v_nb = 0
        obj_name = ""
        f = False
        f_nb = 0
        f_index = 0
        f_mat = {}
        f_uv = {}
        
        for line in fp:
            words = line.split()
            if len(words) == 0:                     ##Nothing
                pass    
            elif words[0] == "}":                       ##end of mat or obj
                dprint('end something', debug)
                if obj:                             ##if end of obj import it in blender
                    if v:
                        v=False
                        dprint('end of vertex', debug)
                    elif f:
                        f=False
                        dprint('end of face', debug)
                    else:
                        dprint('end of obj. importing :"%s"' % obj_name, debug)
                        me = bpy.data.meshes.new(obj_name)
                        me.from_pydata(verts, [], faces)
                        me.update()
                        for mat_tmp in mat_list:
                            me.materials.append(mat_tmp)
                            
                        if len(f_mat):
                            for fmk in f_mat.keys():
                                me.polygons[fmk].material_index = f_mat[fmk]
                                
                        #if len(f_uv):
                            
                            
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
                    faces.append((int(words[1].strip('V(')), int(words[2]), int(words[3].strip(')'))))
                elif f_vert_nb == 4:
                    faces.append((int(words[1].strip('V(')), int(words[2]), int(words[3]), int(words[4].strip(')'))))
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
                                f_uv[f_index] = [ float( words[i].strip("UV(")), float(words[i+1]), float(words[i+2]), float(words[i+3]), float(words[i+4]), float( words[i+5].strip(")"))  ]
                            elif f_vert_nb == 4:
                                f_uv[f_index] = [ float( words[i].strip("UV(")), float(words[i+1]), float(words[i+2]), float(words[i+3]), float(words[i+4]), float(words[i+5]), float(words[i+6]), float( words[i+7].strip(")"))  ]
                            else:
                                dprint('error : face UV with %i vertex' %(f_vert_nb), debug)
                    
                f_index +=1
                f_nb = f_nb -1
                if f_nb ==0:
                    #f= False
                    dprint('end of face?', debug)
            elif mat and mat_nb > 0 :
                mat_tmp = bpy.data.materials.new(words[0].strip('"'))
                mat_tmp.diffuse_color = (float(words[2].strip('col(')), float(words[3]), float(words[4]))
                """mat_tmp.diffuse_intensity = self.diffuse
                mat_tmp.ambient = self.ambient
                mat_tmp.specular_intensity = self.specular"""
                if float(words[5].strip(')')) < 1.0:
                    mat_tmp.use_transparency = True
                    mat_tmpd = float(words[5].strip(')'))
                mat_list.append(mat_tmp)
                
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
 