'''
    Copy Right Notice
    =================
    * This file is part of the Blender Addon "Image Mapper" which is distributed under a EULA License.
    * Redistribute, resell, or lease of the software is strictly prohibited.
    * This software is provided "as is" and without any warranty.
    * Changing or Removing this notice is strictly prohibited.
    * For full license terms, please visit the following link: <Blender addon marketplace holder>
    
    For support, please contact: mohidoart@gmail.com
    (c) 2024 Mohammed Al-Mahdawi.
'''

import bpy
from bpy.props import (IntProperty)
from utils import unbind_materials, clean_materials

class ApplyImageMapping(bpy.types.Operator):
    """Apply Image Mapping based on properties"""
    bl_idname = "object.apply_image_mapping"
    bl_label = "Apply Mapping"

    def execute(self, context):
        props = context.scene.image_mapper_properties
        mat_name = props.general_material.name
        rm_cops = props.cleanup_copied_materials

        self.report({'INFO'}, f"Remove Copies Is Set To: {rm_cops}")
        if(props.cleanup_copied_materials):
            self.report({'INFO'}, f"Unbinding Copies Of Material: {mat_name}")
            unbind_materials(mat_name)
            
            self.report({'INFO'}, f"Removing Copies Of Material: {mat_name}")
            clean_materials(mat_name)

        # Placeholder for the main logic
        self.report({'INFO'}, "Image Mapping Applied")
        return {'FINISHED'}

class AddImagePath(bpy.types.Operator):
    """Add an image file path to the collection."""
    bl_idname = "image_mapper.add_image_path"
    bl_label = "Add Image File Path"

    def execute(self, context):
        item = context.scene.image_mapper_properties.image_files.add()
        item.file_path = ""  # Default or use file browser
        self.report({'INFO'}, "Loading Image Files")
        return {'FINISHED'}

class RemoveImagePath(bpy.types.Operator):
    """Remove an image file path from the collection."""
    bl_idname = "image_mapper.remove_image_path"
    bl_label = "Remove Image File Path"
    index: IntProperty()

    def execute(self, context):
        props = context.scene.image_mapper_properties
        props.image_files.remove(self.index)
        self.report({'INFO'}, "Removing Image Files")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ApplyImageMapping)
    bpy.utils.register_class(AddImagePath)
    bpy.utils.register_class(RemoveImagePath)

def unregister():
    bpy.utils.unregister_class(RemoveImagePath)
    bpy.utils.unregister_class(AddImagePath)
    bpy.utils.unregister_class(ApplyImageMapping)
