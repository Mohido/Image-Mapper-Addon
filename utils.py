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
import re

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



def indexify_paths(paths):
    '''
        Indexify the image paths for the objects.
        Returns the file_name and its full path as a dictionary.
        Example:
        {
            '1.png': '/path/to/1.png',
        }

        @input paths: list of paths (images or directories)
        @output indexed_paths: dictionary of indexed paths
    '''
    indexed_paths = {}
    paths_queue = paths.copy()

    while(len(paths_queue) > 0):
        path = paths_queue.pop(0)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
            
        # Check if it is directory
        if os.path.isdir(path):
            # append the subdirectories to the queue
            for sub in os.listdir(path):
                paths_queue.append(os.path.join(path, sub))
            
        # Check if it is an image file
        elif path.endswith('.png') or path.endswith('.jpg'):
            # Get file name regardless of the operating system
            index = os.path.basename(path)
            indexed_paths[index] = path
    return indexed_paths



def evaluate_expression(exp, oid):
    '''
        Simple function to evaluate a python expression from a string.
        It stricts the execution of the expression to the following variables:
        - oid: object id (int)
        - exp: expression string

        @param exp: the expression to be evaluated
        @param oid: the object index (suffix of the object name)
        @return: the result of the expression

    '''   
    return eval(exp) 

def map_materials(object_pattern, material_ptr, nodes_labels, paths, expressions):
    '''
        Create material copies for the objects that match the pattern.
        Assign copies to mesh objects
        Load images, and assign them to material nodes
    '''

    # Step 0: Validate the input
    if(len(expressions) > len(nodes_labels)):
        raise ValueError("Expressions length should NOT exceed the length of the nodes labels.")


    # Step 1: Iterate over objects and print names
    indexed_paths = indexify_paths(paths)
    for obj in bpy.context.scene.objects:

        # Step 2: Verify and get object index
        if( obj.type != 'MESH' or not obj.name.startswith(object_pattern)):
            print(f"Skipping Non-Mesh Object: {obj.name}")
            continue
        print(f"Mapping Material For Object: {obj.name}")
        obj_index = int(obj.name.split('.')[-1]) if '.' in obj.name else 0

        # Step 2: Creates Material Copy and Insert Slot
        mat_copy = general_material.copy()
        if not mat_copy.use_nodes:
            raise ValueError("Material should 'use nodes'.")

        # Duplicate the general material and apply to the first material slot
        if not obj.material_slots:
            obj.data.materials.append(None)

        # Assign to a new material to the last slot
        obj.material_slots[len(obj.material_slots)-1].material = mat_copy


        # Step 3: Assign Images to Material Nodes
        for i, exp in enumerate(expressions):
            # Transform string to python expression
            image_index = evaluate_expression(exp, obj_index)                       # The name of the image file
            image_path = indexed_paths[image_index]                                 # Extract the image path from the indexed paths
            node = find_node_in_group(mat_copy.node_tree.nodes, nodes_labels[i])    # Find the node in the material nodes
            if not node:
                raise ValueError(f"Node with label: {label} not found in the material nodes.")

            node.image = bpy.data.images.load(image_path)











       


