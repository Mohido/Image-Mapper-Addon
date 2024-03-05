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
from bpy.props import (StringProperty, PointerProperty, BoolProperty, CollectionProperty, IntProperty)
from bpy.types import PropertyGroup, Material

class ImageFilePathItem(PropertyGroup):
    file_path: StringProperty(
        name="Image File Path",
        subtype='FILE_PATH'
    )
    deep: BoolProperty(name="Recursive Search", default=False)


class ExpressionItem(PropertyGroup):
    expression: StringProperty(name="Python Expression: Given Object's suffix (as 'oid' of type integer), return filename. (e.g: f'{oid}.png'")

class NodeLabelItem(PropertyGroup):
    label: StringProperty(name="Image Texture Label")

class ImageMapperProperties(PropertyGroup):
    image_node_labels: CollectionProperty(type=NodeLabelItem)
    expressions: CollectionProperty(type=ExpressionItem)
    image_files: CollectionProperty(type=ImageFilePathItem)
    object_name_pattern: StringProperty(name="Objects Prefix", default="Plane")
    general_material: PointerProperty(name="Material Template", type=Material)
    nested_node_search: BoolProperty(name="Nested Node Search", default=False)
    cleanup_copied_materials: BoolProperty(name="Cleanup Copied Materials", default=False)
    active_image_file_index: IntProperty(name="Active Image File Index")

def register():
    bpy.utils.register_class(ImageFilePathItem)
    bpy.utils.register_class(ExpressionItem)
    bpy.utils.register_class(NodeLabelItem)
    bpy.utils.register_class(ImageMapperProperties)
    bpy.types.Scene.image_mapper_properties = PointerProperty(type=ImageMapperProperties)

def unregister():
    # Unregister the properties doesn't require class unregistration, but rather just deleting the property from the scene/object/... type.
    if hasattr(bpy.types.Scene, 'image_mapper_properties'):
        del bpy.types.Scene.image_mapper_properties
