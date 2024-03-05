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
