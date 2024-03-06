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
import os

LOG_LEVEL = 'INFO'

LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'CRITICAL': 4
}

def log(LEVEL, message):
    if LOG_LEVELS[LEVEL] >= LOG_LEVELS[LOG_LEVEL]:
        print(f"utils.py: LOG_LEVEL: {LEVEL} - {message}")



# Utility functions that support your operators


# Function to find a node by name, even if nested inside a group
def find_node_in_group(nodes, name, nested_search=False):
    for node in nodes:
        log('DEBUG', f"Finding node: {name} in {node.name}")
        if node.type == 'GROUP' and nested_search:
            # Recursively search in group nodes
            found_node = find_node_in_group(node.node_tree.nodes, name, nested_search)
            if found_node:
                return found_node
        elif node.label == name:
            return node
    return None



def unbind_materials(material_name_pattern):
    log('DEBUG', f"Unbinding Copies Of {material_name_pattern}")
    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        # Check each material slot of the object
        for slot in obj.material_slots:
            # If the material slot is not empty and the material name matches the pattern
            if slot.material and '.' in slot.material.name and slot.material.name.startswith(material_name_pattern) and slot.material.name.split('.')[1].isdigit():
                # Clear the material slot
                log('DEBUG', f"Unbound material {slot.material.name} from {obj.name}")
                slot.material = None



def clean_materials(material_name): 
    to_remove = [mat for mat in bpy.data.materials if '.' in mat.name and mat.name.startswith(material_name) and mat.name.split('.')[1].isdigit()]
    log('DEBUG', f"Deleting Copies Of {material_name}")
    # Iterate through all materials in the current blend file
    for mat in to_remove:
        # Check if the material is not used by any objects
        if mat.users == 0:
            log('DEBUG', f"Removing: {mat.name}")
            # Remove the material
            bpy.data.materials.remove(mat)
        else:
           log('DEBUG', f"Cannot remove {mat.name}, it is in use.")



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
        top = paths_queue.pop(0)
        path = top['path']
        deep = top['deep']

        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
            
        # Check if it is directory
        if os.path.isdir(path) and deep:
            # append the subdirectories to the queue
            for sub in os.listdir(path):
                paths_queue.append({
                    "path": os.path.join(path, sub),
                    "deep": deep
                    })
            
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


def find_materials_starting_with(prefix):
    """
    Search for materials in the current scene that start with the given prefix.

    Parameters:
    - prefix (str): The prefix to search for in material names.

    Returns:
    - A list of material names that start with the given prefix.
    """
    for material in bpy.data.materials:
        if material.name.startswith(prefix) and '.' not in material.name:
            return material
    return None


def map_materials(object_pattern, material_name, nodes_labels, paths, expressions, nested_search):
    '''
        Create material copies for the objects that match the pattern.
        Assign copies to mesh objects
        Load images, and assign them to material nodes
    '''
    material_ptr = find_materials_starting_with(material_name)
    if not material_ptr:
        raise ValueError(f"Material with prefix: {material_name} not found.")
    # Step 0: Validate the input
    if(len(expressions) > len(nodes_labels)):
        raise ValueError("Expressions length should NOT exceed the length of the nodes labels.")
    elif(len(paths) < 1):
        log('WARNING', "No paths found to map materials.")
        return
    elif(len(nodes_labels) < 1):
        log('WARNING', "No node labels found to map materials.")
        return
    elif(len(expressions) < 1):
        log('WARNING', "No expression logic found to map materials.")
        return

    # Step 1: Iterate over objects and print names
    
    indexed_paths = indexify_paths(paths)
    for obj in bpy.context.scene.objects:

        # Step 2: Verify and get object index
        if( obj.type != 'MESH' or not obj.name.startswith(object_pattern)):
            log('DEBUG', f"Skipping Non-Mesh Object: {obj.name}")
            continue
        log('INFO', f"Mapping Material For Object: {obj.name}")
        obj_index = int(obj.name.split('.')[-1]) if '.' in obj.name else 0

        # Step 2: Creates Material Copy and Insert Slot
        mat_copy = material_ptr.copy()
        if not mat_copy.use_nodes:
            raise ValueError("Material should 'use nodes'.")

        # Step 3: Assign Images to Material Nodes
        for i, exp in enumerate(expressions):
            # Transform string to python expression
            node = find_node_in_group(mat_copy.node_tree.nodes, nodes_labels[i], nested_search)    # Find the node in the material nodes
            if not node:
                raise ValueError(f"Node with label: {nodes_labels[i]} not found in the material nodes.")
            image_index = evaluate_expression(exp, obj_index)                                   # The name of the image file
            image_path = indexed_paths.get(image_index, None)                                   # Extract the image path from the indexed paths
            if image_path:
                node.image = bpy.data.images.load(image_path)
            else:
                log('WARNING', f"File '{image_index}' Can't Be Found")
        
        # Step 4: Assign the material to the object
        # Duplicate the general material and apply to the first material slot
        if not obj.material_slots:
            obj.data.materials.append(mat_copy)
            continue

        # Searches for first empty slot and assigns the material. If material exists, it will be replaced.
        assigned = False
        for slot in obj.material_slots:
            if not slot.material or slot.material.name.startswith(material_ptr.name):
                slot.material = mat_copy
                assigned = True
                break
        
        # Assign to a new material to a new slot
        if not assigned:
            obj.data.materials.append(mat_copy)

        log('DEBUG', "\n\n=====================\n\n")











       


