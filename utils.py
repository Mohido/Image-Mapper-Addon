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

# Utility functions that support your operators


# Function to find a node by name, even if nested inside a group
def find_node_in_group(nodes, name):
    for node in nodes:
        print(f"Finding node: {name} in {node.label}")
        if node.type == 'GROUP':
            # Recursively search in group nodes
            found_node = find_node_in_group(node.node_tree.nodes, name)
            if found_node:
                return found_node
        elif node.label == name:
            return node
    return None



def unbind_materials(material_name_pattern):
    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        # Check each material slot of the object
        for slot in obj.material_slots:
            # If the material slot is not empty and the material name matches the pattern
            if slot.material and '.' in slot.material.name and slot.material.name.startswith(material_name_pattern) and slot.material.name.split('.')[1].isdigit():
                # Clear the material slot
                slot.material = None
                print(f"Unbound material {slot.name} from {obj.name}")



def clean_materials(material_name): 
    to_remove = [mat for mat in bpy.data.materials if '.' in mat.name and mat.name.startswith(material_name) and mat.name.split('.')[1].isdigit()]

    # Iterate through all materials in the current blend file
    for mat in to_remove:
        # Check if the material is not used by any objects
        if mat.users == 0:
            print(f"Removing: {mat.name}")
            # Remove the material
            bpy.data.materials.remove(mat)
        else:
            print(f"Cannot remove {mat.name}, it is in use.")

