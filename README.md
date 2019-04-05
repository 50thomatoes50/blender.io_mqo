blender.io_mqo : Blender importer and exporter for Metasequoia files (.mqo)
==============
![ALPHA](https://badgen.net/badge/Status/Alpha/red)
![GNU GPL V2](https://badgen.net/github/license/50thomatoes50/blender.io_mqo)

Features | Import | Export
--- | --- | --- |
Basic geometry (vert,edge,tri,quad) |  :heavy_check_mark: |  :heavy_check_mark:
UV map  |  :heavy_check_mark: |  :heavy_check_mark:
Materials  |  :heavy_check_mark: |  :heavy_check_mark:
Simple Modifier (Mirror / subdivision surface)  |  :soon: |  :heavy_check_mark:


Todo
--------------
- Port to bpy 2.8
- Export other thing like text (but converted in mesh) note: not sure to add this feature
- Importer Modifier (Mirror / subdivision surface)
- Metasequoia 4+ featues :
  - Use `bpy.Bmesh` to support face with 4+ vertices
  - Bones


___
# Installation method
- Click `Download ZIP`
- Extract the folder `io_scene_mqo` in your blender folder installation (eg: "`...\Blender2.##\scripts\addons\`"
- Start blender
- Go `File` >> `User preferences...` >> `Addons` >> `Import-Export` and check the tick at `Import-Export: Metasequoia format(.mqo)`

# Usage
- In blender, go to `File` and you will see `Metasequoia (.mqo)` in `Export` and `Import` menu
