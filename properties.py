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
    del bpy.types.Scene.image_mapper_properties
    bpy.utils.unregister_class(ImageMapperProperties)
    bpy.utils.unregister_class(ImageFilePathItem)
