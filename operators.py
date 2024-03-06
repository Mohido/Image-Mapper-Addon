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
from .utils import unbind_materials, clean_materials, map_materials

class ApplyImageMapping(bpy.types.Operator):
    """Apply Image Mapping based on properties"""
    bl_idname = "object.apply_image_mapping"
    bl_label = "Apply Mapping"

    def execute(self, context):
        props = context.scene.image_mapper_properties

        # Single Values
        mat = props.general_material
        obj_name = props.object_name_pattern
        rm_cops = props.cleanup_copied_materials
        nested_search = props.nested_node_search
        # Lists
        node_labels = [x.label for x in props.image_node_labels]
        expressions = [x.expression for x in props.expressions]
        paths = [{'path': bpy.path.abspath(x.file_path), 'deep': x.deep} for x in props.image_files]

        # Delete Material Copies
        if(props.cleanup_copied_materials):
            unbind_materials(mat)
            clean_materials(mat)
        
        # Map Materials
        map_materials(obj_name, mat, node_labels, paths, expressions, nested_search)
        
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

class AddExpression(bpy.types.Operator):
    """Add an expression to the collection."""
    bl_idname = "image_mapper.add_expression"
    bl_label = "Add Expression"

    def execute(self, context):
        item = context.scene.image_mapper_properties.expressions.add()
        item.expression = ""  # Default or use file browser
        self.report({'INFO'}, "Adding Expression")
        return {'FINISHED'}

class RemoveExpression(bpy.types.Operator):
    """Remove an expression from the collection."""
    bl_idname = "image_mapper.remove_expression"
    bl_label = "Remove Expression"
    index: IntProperty()

    def execute(self, context):
        props = context.scene.image_mapper_properties
        props.expressions.remove(self.index)
        self.report({'INFO'}, "Removing Expression")
        return {'FINISHED'}
    
class AddNodeLabel(bpy.types.Operator):
    """Add an image node label to the collection."""
    bl_idname = "image_mapper.add_node_label"
    bl_label = "Add Image Node Label"

    def execute(self, context):
        item = context.scene.image_mapper_properties.image_node_labels.add()
        item.label = ""  # Default or use file browser
        self.report({'INFO'}, "Adding Image Node Label")
        return {'FINISHED'}
    
class RemoveNodeLabel(bpy.types.Operator):
    """Remove an image node label from the collection."""
    bl_idname = "image_mapper.remove_node_label"
    bl_label = "Remove Image Node Label"
    index: IntProperty()

    def execute(self, context):
        props = context.scene.image_mapper_properties
        props.image_node_labels.remove(self.index)
        self.report({'INFO'}, "Removing Image Node Label")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ApplyImageMapping)
    bpy.utils.register_class(AddImagePath)
    bpy.utils.register_class(RemoveImagePath)
    bpy.utils.register_class(AddExpression)
    bpy.utils.register_class(RemoveExpression)
    bpy.utils.register_class(AddNodeLabel)
    bpy.utils.register_class(RemoveNodeLabel)

def unregister():
    bpy.utils.unregister_class(RemoveImagePath)
    bpy.utils.unregister_class(AddImagePath)
    bpy.utils.unregister_class(ApplyImageMapping)
    bpy.utils.unregister_class(AddExpression)
    bpy.utils.unregister_class(RemoveExpression)
    bpy.utils.unregister_class(AddNodeLabel)
    bpy.utils.unregister_class(RemoveNodeLabel)