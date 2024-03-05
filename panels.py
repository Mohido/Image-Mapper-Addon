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

class ImageMapperPanel(bpy.types.Panel):
    """Creates a Panel for the Image Mapper"""
    bl_label = "Image Mapper"
    bl_idname = "OBJECT_PT_image_mapper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Image Mapper'

    def draw(self, context):
        layout = self.layout
        props = context.scene.image_mapper_properties

        layout.prop(props, "object_name_pattern")
        layout.prop(props, "general_material")
        layout.prop(props, "mapping_expression")
        layout.prop(props, "nested_node_search")
        layout.prop(props, "cleanup_copied_materials")

        layout.label(text="Image Files:")
        for i, image_file in enumerate(props.image_files):
            box = layout.box()
            row = box.row()
            row.prop(image_file, "file_path", text="")
            row.operator("image_mapper.remove_image_path", icon='X', text="").index = i
        
        layout.operator("image_mapper.add_image_path", icon='ADD', text="Add Image File")
        layout.operator("object.apply_image_mapping")

def register():
    bpy.utils.register_class(ImageMapperPanel)

def unregister():
    bpy.utils.unregister_class(ImageMapperPanel)
