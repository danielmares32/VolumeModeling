# VolumeModeling

This project provides tools for 3D mesh volume calculation, scaling, and analysis. It includes functions to calculate the voxel volume of a 3D mesh from an OBJ file, scale a 3D mesh to a target volume, calculate the compactness of a 3D voxel array, and find the number of positive voxels. The project also implements the Hungarian algorithm for optimal assignment, which can be useful in comparing different 3D models (The ones in the "Combined CAD Objects"). These tools can be useful in various fields such as computer graphics, game development, 3D printing, and computational geometry.

# 3D Mesh Volume Calculation and Scaling (volumen.py file)

## Dependencies
- trimesh
- os
- subprocess
- numpy
- binvox_rw

## Functions

### calculate_voxel_volume(obj_file)
Calculates the voxel volume of a 3D mesh from an OBJ file.

### scale_to_volume(obj_file, target_volume, tolerance=100)
Scales a 3D mesh from an OBJ file to a target volume, within a specified tolerance.

## Usage
```python
import volumen

# Replace 'cube.obj' with the path to your OBJ file
obj_file_path = 'cube.obj'

try:
    volumen.scale_to_volume(obj_file_path, 9824)
    voxel_volume = volumen.calculate_voxel_volume(obj_file_path)
    print(f"The voxel volume of the OBJ file is: {voxel_volume} cubic units.")
except Exception as e:
    print(f"An error occurred: {e}")
    
```

# 3D Mesh Processing and Analysis (alg.py)

## Dependencies
- numpy
- os
- trimesh
- scipy

## Functions

### Cad(m1, file)
Writes non-zero coordinates in `m1` to a file.

### mesh_to_voxels(mesh, voxel_size=1)
Converts a 3D mesh into a voxel representation.

### pad_voxels(voxels, target_shape)
Pads a 3D voxel array to a target shape with zeros.

### calculate_discrete_compactness(voxels)
Calculates the discrete compactness of a 3D voxel array.

### find_obj_files(directory)
Finds all .obj files in a given directory.

### calculate_cost_matrix(voxels1, voxels2)
Calculates a cost matrix based on the Euclidean distance between two sets of voxels.

### calculate_work(voxels1, voxels2, obj_file)
Calculates the total work required to transform one set of voxels into another.

## Usage
```python
import alg
import trimesh

# Load a 3D mesh
mesh = trimesh.load_mesh('model.obj')

# Convert the mesh to voxels
voxels = alg.mesh_to_voxels(mesh)

# Pad the voxels to a target shape
padded_voxels = alg.pad_voxels(voxels, (100, 100, 100))

# Calculate the discrete compactness
compactness = alg.calculate_discrete_compactness(padded_voxels)

# Find all .obj files in a directory
obj_files = alg.find_obj_files('/path/to/directory')

# Calculate the cost matrix between two sets of voxels
cost_matrix = alg.calculate_cost_matrix(voxels, padded_voxels)

# Calculate the total work required to transform one set of voxels into another
total_work = alg.calculate_work(voxels, padded_voxels, 'model.obj')

```

# 3D Mesh Processing and Analysis (Main_src.py)

This Python script aligns 3D meshes using PCA, calculates their compactness, and compares them.

## Dependencies
- trimesh
- numpy
- os
- sklearn
- alg (custom module)

## Functions

### align_mesh_with_pca(mesh)
Aligns a 3D mesh using PCA.

## Usage
```python
import trimesh
import numpy as np
import os
from sklearn.decomposition import PCA
import alg

def align_mesh_with_pca(mesh):
    # Function body...

# Set your working directory
directory = './your_directory/'

# Find all .obj files in the directory
obj_files = alg.find_obj_files(directory)

# Process each .obj file
for obj_file in obj_files:
    # Load the mesh
    mesh = trimesh.load_mesh(obj_file)
    
    # Align the mesh with PCA
    aligned_mesh = align_mesh_with_pca(mesh)
    
    # Convert the mesh to voxels
    voxels = alg.mesh_to_voxels(aligned_mesh)
    
    # Calculate the compactness
    compactness = alg.calculate_discrete_compactness(voxels)
    
    # Print the compactness
    print(f"{obj_file}: {compactness}")

```

# 3D Mesh Processing and Analysis (Main_work.py)

This Python script aligns 3D meshes using PCA, calculates their compactness, and compares them.

## Dependencies
- trimesh
- numpy
- os
- pandas
- concurrent.futures
- sklearn.decomposition
- alg (custom module)

## Functions

### align_mesh_with_pca(mesh)
Aligns a 3D mesh using PCA.

### process_file(obj_file, max_compactness_file, voxels1, results, is_same_file)
Processes each file and calculates the results.

## Usage
```python
import trimesh
import numpy as np
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from sklearn.decomposition import PCA
import alg 

def align_mesh_with_pca(mesh):
    # Function body...

def process_file(obj_file, max_compactness_file, voxels1, results, is_same_file):
    # Function body...

# Set your working directory
directory = './your_directory/'

# Find all .obj files in the directory
obj_files = alg.find_obj_files(directory)

# Process each .obj file
for obj_file in obj_files:
    # Load the mesh
    mesh = trimesh.load_mesh(obj_file)
    
    # Align the mesh with PCA
    aligned_mesh = align_mesh_with_pca(mesh)
    
    # Convert the mesh to voxels
    voxels = alg.mesh_to_voxels(aligned_mesh)
    
    # Calculate the compactness
    compactness = alg.calculate_discrete_compactness(voxels)
    
    # Print the compactness
    print(f"{obj_file}: {compactness}")

# Process files in parallel and save results to an Excel file
with ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(process_file, obj_file, max_compactness_file, voxels1, results, obj_file == max_compactness_file)
        for obj_file in obj_files
    ]
    for future in futures:
        future.result()  # Wait for each task to finish

# Create a pandas DataFrame and save as an Excel file
df = pd.DataFrame(results)
df.to_excel('Results.xlsx', index=False)

print("Results saved in 'Results.xlsx'")

```