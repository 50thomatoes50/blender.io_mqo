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

# <pep8-80 compliant>

bl_info = {
    "name": "Metasequoia format (.mqo)",
    "author": "50thomatoes50",
    "blender": (2, 65, 0),
    "location": "File > Import-Export",
    "description": "Import-Export MQO, UV's, "
                   "materials and textures",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/Import-Export/MQO",
    "tracker_url": "https://github.com/50thomatoes50/blender.io_mqo/issues",
    "category": "Import-Export"}


#http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Multi-File_packages#init_.py
if "bpy" in locals():
    import imp
    #if "import_mqo" in locals():
    #    imp.reload(import_mqo)
    if "export_mqo" in locals():
        imp.reload(export_mqo)


import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       )
from bpy_extras.io_utils import (ExportHelper,
                                 path_reference_mode,
                                 axis_conversion,
                                 )


class ExportMQO(bpy.types.Operator, ExportHelper):
    bl_idname = "io_export_scene.mqo"
    bl_description = 'Export from mqo file format (.mqo)'
    bl_label = "Export mqo"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
 
    # From ExportHelper. Filter filenames.
    filename_ext = ".mqo"
    filter_glob = StringProperty(default="*.mqo", options={'HIDDEN'})
 
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for exporting the mqo file", 
        maxlen= 1024, default= "")
 
    rot90 = bpy.props.BoolProperty(
        name = "Rotate 90 degrees",
        description="Rotate mesh to Y up",
        default = True)
 
    scale = bpy.props.FloatProperty(
        name = "Scale", 
        description="Scale mesh", 
        default = 1, min = 0.001, max = 1000.0)
 
    def execute(self, context):
        print("Load", self.properties.filepath)
        from . import export_mqo
        export_mqo.export_mqo(
            self.properties.filepath, 
            context.object, 
            self.rot90, 
            1.0/self.scale)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


'''def menu_func_import(self, context):
    self.layout.operator(ImportMQO.bl_idname, text="Metasequoia (.mqo)")
'''

def menu_func_export(self, context):
    self.layout.operator(ExportMQO.bl_idname, text="Metasequoia (.mqo)")


def register():
    bpy.utils.register_module(__name__)

    #bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    #bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
