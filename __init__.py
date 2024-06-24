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

bl_info = {
    "name": "Image Mapper",
    "blender": (3, 0, 0),
    "category": "Object",
    "description": "Maps images to materials based on object naming patterns.",
    "author": "Mohammed Al-Mahdawi - mohidoart@gmail.com",
    "version": (1, 0),
    "location": "View3D > Sidebar > Image Mapper Tab",
}

from . import operators, panels, properties


### NOTE DEBUG STARTS {MOHAMMED}: This is kept for debugging purposes.
# import importlib
# importlib.reload(utils)
# importlib.reload(operators)
# importlib.reload(panels)
# importlib.reload(properties)

### DEBUG ENDS

def register():
    properties.register()
    operators.register()
    panels.register()

def unregister():
    properties.unregister()
    panels.unregister()
    operators.unregister()


if __name__ == "__main__":

    ### NOTE DEBUG STARTS {MOHAMMED}: This is kept for debugging purposes.
    # import os
    # os.system('cls')
    ### DEBUG ENDS

    try:
        unregister()
    except:
        pass
    register()
