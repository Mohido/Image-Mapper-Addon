bl_info = {
    "name": "Image Mapper",
    "blender": (2, 93, 0),
    "category": "Object",
    "description": "Maps images to materials based on object naming patterns.",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > Image Mapper Tab",
}


import operators, panels, properties

def register():
    properties.register()
    operators.register()
    panels.register()

def unregister():
    properties.unregister()
    operators.unregister()
    panels.unregister()

if __name__ == "__main__":
    import os
    os.system('cls')
    register()
