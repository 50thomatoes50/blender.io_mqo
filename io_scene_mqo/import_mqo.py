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
 
def import_simple_obj(filepath, rot90, scale):
    name = os.path.basename(filepath)
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, 'rU')    # Universal read
    print('Importing %s' % realpath)
 
    verts = []
    faces = []
    texverts = []
    texfaces = []
 
    for line in fp:
        words = line.split()
        if len(words) == 0:
            pass
        elif words[0] == 'v':
            (x,y,z) = (float(words[1]), float(words[2]), float(words[3]))
            if rot90:
                verts.append( (scale*x, -scale*z, scale*y) )
            else:
                verts.append( (scale*x, scale*y, scale*z) )
        elif words[0] == 'vt':
            texverts.append( (float(words[1]), float(words[2])) )
        elif words[0] == 'f':
            (f,tf) = parseFace(words)
            faces.append(f)
            if tf:
                texfaces.append(tf)
        else:
            pass
    print('%s successfully imported' % realpath)
    fp.close()
 
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
 
    if texverts:
        uvtex = me.uv_textures.new()
        uvtex.name = name
        data = uvtex.data
        for n in range(len(texfaces)):
            tf = texfaces[n]
            data[n].uv1 = texverts[tf[0]]
            data[n].uv2 = texverts[tf[1]]
            data[n].uv3 = texverts[tf[2]]
            if len(tf) == 4:
                data[n].uv4 = texverts[tf[3]]
 
    scn = bpy.context.scene
    ob = bpy.data.objects.new(name, me)
    scn.objects.link(ob)
    scn.objects.active = ob
 
    return
 
def parseFace(words):
    face = []
    texface = []
    for n in range(1, len(words)):
        li = words[n].split('/')
        face.append( int(li[0])-1 )
        try:
            texface.append( int(li[1])-1 )
        except:
            pass
    return (face, texface)