import bpy
from bpy.props import (IntProperty)

class ApplyImageMapping(bpy.types.Operator):
    """Apply Image Mapping based on properties"""
    bl_idname = "object.apply_image_mapping"
    bl_label = "Apply Mapping"

    def execute(self, context):
        props = context.scene.image_mapper_properties
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
    bpy.utils.unregister_class(ApplyImageMapping)
    bpy.utils.unregister_class(AddImagePath)
    bpy.utils.unregister_class(RemoveImagePath)
