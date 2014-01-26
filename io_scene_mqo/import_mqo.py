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

import bpy, os

def dprint(string):
    debug = True
    if debug:
        print(string)
    return
    
    
def import_mqo(filepath, rot90, scale):
    name = os.path.basename(filepath)
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, 'rU')    # Universal read
    print('Importing %s' % realpath)
 
    verts = []
    faces = []
    edges = []
    texverts = []
    texfaces = []
    obj = False
    mat = False
    mat_nb = 0
    v = False
    v_nb = 0
    obj_name = ""
    f = False
    f_nb = 0
    
    for line in fp:
        words = line.split()
        if len(words) == 0:                     ##Nothing
            pass    
        elif words[0] == "}":                       ##end of mat or obj
            dprint('end something')
            if obj:                             ##if end of obj import it in blender
                if v:
                    v=False
                    dprint('end of vertex')
                elif f:
                    f=False
                    dprint('end of face')
                else:
                    dprint('end of obj. importing :"%s"' % obj_name)
                    me = bpy.data.meshes.new(obj_name)
                    me.from_pydata(verts, [], faces)
                    me.update()
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
                    verts = []
                    faces = []
                    texverts = []
                    texfaces = []
            if mat:                             ##if end of mat import later in obj
                dprint('end of mat')
                mat = False
                
        elif words[0] == 'Object':              ##detect an object
            dprint('begin of obj :%s' % words[1])
            obj = True
            obj_name = words[1].strip('"')
        elif words[0] == 'Material':            ##detect materials
            dprint('begin of mat')
            mat = True
            mat_nb = int(words[1].strip('"'))
        elif obj and words[0] == "vertex":      ##detect vertex when obj
            dprint('begin of ver')
            v = True
            v_nb = int(words[1])
        elif obj and v and v_nb != 0:           ##get vertex coor when vertex and obj
            dprint('found a vertex')
            (x,y,z) = (float(words[0]), float(words[1]), float(words[2]))
            if rot90:
                verts.append( (scale*x, scale*z, scale*y) )
            else:
                verts.append( (scale*x, scale*y, scale*z) )
            v_nb = v_nb -1
            if v_nb == 0:                       
                #v = False
                dprint('end of vertex?')
        elif obj and words[0] == "face":        ##detect face when obj
            dprint('begin of face')
            f = True
            f_nb = int(words[1])
        elif obj and f and f_nb != 0:           ##get face vertex
            dprint('found a face')
            if int(words[0]) == 2:
                edges.append((int(words[1].strip('V(')), int(words[2].strip(')'))))
            elif int(words[0]) == 3:
                faces.append((int(words[1].strip('V(')), int(words[2]), int(words[3].strip(')'))))
            elif int(words[0]) == 4:
                faces.append((int(words[1].strip('V(')), int(words[2]), int(words[3]), int(words[4].strip(')'))))
            else:
                dprint('error : face with %i vertex' % words[0])
            f_nb = f_nb -1
            if f_nb ==0:
                #f= False
                dprint('end of face?')
        else:
            dprint('don\'t know what is it')
            pass            

    print('%s successfully imported' % realpath)
    fp.close()
 

 
    return
 
