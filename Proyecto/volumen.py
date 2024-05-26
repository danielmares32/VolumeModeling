import trimesh
import os
import subprocess
import numpy as np
import binvox_rw
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def convert_obj_to_binvox_and_calculate_volume(obj_file, binvox_exe_path):
    """
    Convert a .obj file to a .binvox file and calculate the volume in voxels.

    Parameters:
    obj_file (str): Path to the .obj file.
    binvox_exe_path (str): Path to the binvox executable.

    Returns:
    int: The volume in voxels.
    """
    # Construct the output file path
    binvox_file = os.path.splitext(obj_file)[0] + '.binvox'

    # Call the binvox executable
    subprocess.call([binvox_exe_path, '-d', '256', obj_file])

    # Open the .binvox file
    with open(binvox_file, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)

    # Calculate the volume in voxels
    volume = np.sum(model.data)

    return volume

def calculate_voxel_volume(obj_file):
    # Load OBJ file
    mesh = trimesh.load_mesh(obj_file)

    # Compute the volume of the mesh
    volume = mesh.voxelized(pitch=1).volume

    return volume

def calculate_discrete_compactness(mesh):
    """
    Calculate the discrete compactness of an object.

    Discrete compactness is defined as the ratio of the volume of the object to the volume of a bounding box that tightly fits the object.

    Parameters:
    mesh (trimesh.Trimesh): The mesh of the object.

    Returns:
    float: The discrete compactness of the object.
    """
    # Calculate the volume of the object
    volume = mesh.volume

    # Calculate the dimensions of the bounding box
    bounding_box_extents = mesh.extents

    # Check if bounding_box_extents has 3 elements
    if len(bounding_box_extents) < 3:
        raise ValueError("The mesh does not have 3 dimensions.")

    # Calculate the volume of the bounding box
    bounding_box_volume = bounding_box_extents[0] * bounding_box_extents[1] * bounding_box_extents[2]
    print(f"Bounding box volume: {bounding_box_volume} = {bounding_box_extents[0]} * {bounding_box_extents[1]} * {bounding_box_extents[2]}")

    # Calculate the discrete compactness
    discrete_compactness = volume / bounding_box_volume

    return discrete_compactness


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

def align_meshes_with_pca(mesh1, mesh2):
    """
    Align two meshes using PCA.

    Parameters:
    mesh1 (trimesh.Trimesh): The first mesh.
    mesh2 (trimesh.Trimesh): The second mesh.

    Returns:
    tuple: Aligned meshes (aligned_mesh1, aligned_mesh2).
    """
    points1 = mesh1.vertices
    points2 = mesh2.vertices

    pca1 = PCA(n_components=3)
    pca2 = PCA(n_components=3)

    pca1.fit(points1)
    pca2.fit(points2)

    aligned_points1 = pca1.transform(points1)
    aligned_points2 = pca2.transform(points2)

    # Crear mallas alineadas
    aligned_mesh1 = trimesh.Trimesh(vertices=aligned_points1, faces=mesh1.faces)
    aligned_mesh2 = trimesh.Trimesh(vertices=aligned_points2, faces=mesh2.faces)

    return aligned_mesh1, aligned_mesh2

def visualize_meshes(aligned_mesh1, aligned_mesh2):
    fig = plt.figure(figsize=(12, 6))

    # Aligned meshes
    ax1 = fig.add_subplot(223, projection='3d')
    plot_mesh(ax1, aligned_mesh1, "Aligned mesh 1")

    ax2 = fig.add_subplot(224, projection='3d')
    plot_mesh(ax2, aligned_mesh2, "Aligned mesh 2")

    plt.show()

def plot_mesh(ax, mesh, title):
    ax.set_title(title)
    ax.add_collection3d(Poly3DCollection(mesh.triangles, alpha=0.1, edgecolor='k'))
    scale = mesh.vertices.flatten()
    ax.auto_scale_xyz(scale, scale, scale)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


# Replace 'example.obj' with the path to your OBJ file
obj_file_path = 'cube.obj'
#obj_file_path = 'Proyecto/Objetos/Banca_9824.obj' test_alignment

#obj_file_path2 = 'Proyecto/Objetos/Chica_9824.obj' test_alignment



try:
    
    #original_mesh1 = trimesh.load_mesh(obj_file_path) test_alignment
    #original_mesh2 = trimesh.load_mesh(obj_file_path2) test_alignment

    # Scale meshes to target volume
    #target_volume = 9824
    #scaled_mesh1 = scale_to_volume(obj_file_path, target_volume) test_alignment
    #scaled_mesh2 = scale_to_volume(obj_file_path2, target_volume) test_alignment

    # Align meshes using PCA
    #aligned_mesh1, aligned_mesh2 = align_meshes_with_pca(scaled_mesh1, scaled_mesh2) test_alignment

    #visualize_meshes(aligned_mesh1, aligned_mesh2) test_alignment   
    #mesh = trimesh.load_mesh(obj_file_path)
    #compactness = calculate_discrete_compactness(mesh)
    #print(f"The discrete compactness of the object is: {compactness}")
    #scale_to_volume(obj_file_path, 9824)
    #convert_obj_to_binvox_and_calculate_volume(obj_file_path, '/Users/danielmares/Downloads/binvox')
    voxel_volume = calculate_voxel_volume(obj_file_path)


    #voxel_volume2 = calculate_voxel_volume('scaled_' + obj_file_path)
    #print(f"The voxel volume of the OBJ file is: {voxel_volume} cubic units.")
    #print(f"The voxel volume of the OBJ file is: {voxel_volume2} cubic units.")
except Exception as e:
    print(f"An error occurred: {e.__traceback__.tb_frame.f_globals['__file__']}: {e.__class__.__name__}: {e.with_traceback(None)}")