blender.io_mqo : Blender importer and exporter for Metasequoia files (.mqo)
==============
![ALPHA](https://badgen.net/badge/Status/Alpha/red)
![GNU GPL V2](https://badgen.net/github/license/50thomatoes50/blender.io_mqo)

Features | Import | Export
--- | --- | --- |
Basic geometry (vert,edge,tri,quad) |  :heavy_check_mark: |  :heavy_check_mark:
UV map  |  :heavy_check_mark: |  :heavy_check_mark:
Materials  |  :x: |  :x: This is broken since the port to 2.80
Simple Modifier (Mirror / subdivision surface)  |  :soon: |  :heavy_check_mark:


Todo
--------------
- Fix material import/export
- Metasequoia 4+ featues :
  - Use `bpy.Bmesh` to support face with 4+ vertices
  - Bones and Animation


___
# Installation method
- Click [`releases`](https://github.com/50thomatoes50/blender.io_mqo/releases)
- Download the latest Zip ( **DO NOT USE** `Source Code (zip)` )
- Start blender
- Go to the menu bar `Edit` >> `Preferences...` >> `Add-ons`
- Click the `Install...` button and use the zip downloaded previously
- You should only see `Import-Export: Metasequoia format(.mqo)`, you need to enable it.

# Usage
- In blender, go to `File` and you will see `Metasequoia (.mqo)` in `Export` and `Import` menu
