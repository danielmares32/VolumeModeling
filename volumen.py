import trimesh
import os
import subprocess
import numpy as np
import binvox_rw

def calculate_voxel_volume(obj_file):
    # Load OBJ file
    mesh = trimesh.load_mesh(obj_file)

    # Compute the volume of the mesh
    volume = mesh.voxelized(pitch=1).volume

    return volume


def scale_to_volume(obj_file, target_volume, tolerance=100):
    # Load OBJ file
    mesh = trimesh.load_mesh(obj_file)

    # Compute the volume of the mesh
    current_volume = calculate_voxel_volume(obj_file)
    print(f"Current volume: {current_volume} cubic units")
    while abs(current_volume - target_volume) > tolerance:
        # Calculate the scale factor
        scale_factor = (target_volume / current_volume) ** (1/3)

        # Scale the mesh
        mesh.apply_scale([scale_factor]*3)

        # Save the scaled mesh
        mesh.export('scaled_' + obj_file)

        # Recalculate the current volume
        current_volume = calculate_voxel_volume('scaled_' + obj_file)
        print(f"Current volume: {current_volume} cubic units")

    return mesh

# Replace 'example.obj' with the path to your OBJ file
obj_file_path = 'cube.obj'



try:
    mesh = trimesh.load_mesh(obj_file_path)
    scale_to_volume(obj_file_path, 9824)
    voxel_volume = calculate_voxel_volume(obj_file_path)
    voxel_volume2 = calculate_voxel_volume('scaled_' + obj_file_path)
    print(f"The voxel volume of the OBJ file is: {voxel_volume} cubic units.")
    print(f"The voxel volume of the OBJ file is: {voxel_volume2} cubic units.")
except Exception as e:
    print(f"An error occurred: {e.__traceback__.tb_frame.f_globals['__file__']}: {e.__class__.__name__}: {e.with_traceback(None)}")
