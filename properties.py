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

class ImageMapperProperties(PropertyGroup):
    object_name_pattern: StringProperty(name="OName", default="*")
    general_material: PointerProperty(name="MName", type=Material)
    image_node_labels: CollectionProperty(name="Image Node Labels", type=ImageFilePathItem)
    mapping_expression: StringProperty(name="Mapping Expression", default="[]")
    nested_node_search: BoolProperty(name="Nested Node Search", default=False)
    cleanup_copied_materials: BoolProperty(name="Cleanup Copied Materials", default=False)
    image_files: CollectionProperty(type=ImageFilePathItem)
    active_image_file_index: IntProperty(name="Active Image File Index")

def register():
    bpy.utils.register_class(ImageFilePathItem)
    bpy.utils.register_class(ImageMapperProperties)
    bpy.types.Scene.image_mapper_properties = PointerProperty(type=ImageMapperProperties)

def unregister():
    # Unregister the properties doesn't require class unregistration, but rather just deleting the property from the scene/object/... type.
    if hasattr(bpy.types.Scene, 'image_mapper_properties'):
        del bpy.types.Scene.image_mapper_properties
