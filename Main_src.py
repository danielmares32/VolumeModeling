import trimesh
import numpy as np
import os
from sklearn.decomposition import PCA
import alg

# Función para alinear mallas con PCA
def align_mesh_with_pca(mesh):
    points = mesh.vertices - mesh.centroid
    pca = PCA(n_components=3)
    aligned_points = pca.fit_transform(points)
    aligned_mesh = trimesh.Trimesh(vertices=aligned_points, faces=mesh.faces)
    return aligned_mesh

# Directorio de trabajo
directory = './objetos/'

# Encontrar todos los archivos .obj en el directorio
obj_files = alg.find_obj_files(directory)

# Calcular la compacidad de cada archivo .obj y encontrar el de mayor compacidad
max_compactness = -1
max_compactness_file = None
compactness_values = {}

for obj_file in obj_files:
    print(f"Procesando archivo: {obj_file}")
    mesh = trimesh.load_mesh(obj_file)
    aligned_mesh = align_mesh_with_pca(mesh)
    voxels = alg.mesh_to_voxels(aligned_mesh)
    compactness = alg.calculate_discrete_compactness(voxels)
    compactness_values[obj_file] = compactness
    if compactness > max_compactness:
        max_compactness = compactness
        max_compactness_file = obj_file

# Imprimir resultados de compacidad
print("\nResultados de compacidad:")
for obj_file, compactness in compactness_values.items():
    print(f"{obj_file}: {compactness}")

print(f"Archivo con mayor compacidad: {max_compactness_file} con compacidad {max_compactness}")

# Cargar el archivo con la mayor compacidad
mesh1 = trimesh.load_mesh(max_compactness_file)
aligned_mesh1 = align_mesh_with_pca(mesh1)
voxels1 = alg.mesh_to_voxels(aligned_mesh1)

# Comparar con cada uno de los archivos, incluido el mismo
for obj_file in obj_files:
    mesh2 = trimesh.load_mesh(obj_file)
    aligned_mesh2 = align_mesh_with_pca(mesh2)
    voxels2 = alg.mesh_to_voxels(aligned_mesh2)
    
    # Determinar el tamaño máximo de la matriz voxelizada
    max_shape = (
        max(voxels1.shape[0], voxels2.shape[0]),
        max(voxels1.shape[1], voxels2.shape[1]),
        max(voxels1.shape[2], voxels2.shape[2])
    )

    # Ajustar el tamaño de las matrices voxelizadas
    voxels1_padded = alg.pad_voxels(voxels1, max_shape)
    voxels2_padded = alg.pad_voxels(voxels2, max_shape)
    
    # Buscar los voxeles positivos con lógica de conjuntos
    voxeles_positivos_1_vs_2 = np.logical_and(voxels1_padded, np.logical_not(voxels2_padded))
    voxeles_positivos_2_vs_1 = np.logical_and(voxels2_padded, np.logical_not(voxels1_padded))
    
    # Crear los archivos de los objetos para visualización
    base_name1 = os.path.basename(max_compactness_file).split('.')[0]
    base_name2 = os.path.basename(obj_file).split('.')[0]
    alg.Cad(voxeles_positivos_1_vs_2, f"Vox+_{base_name1}_VS_{base_name2}")
    alg.Cad(voxeles_positivos_2_vs_1, f"Vox+_{base_name2}_VS_{base_name1}")
    alg.Cad(voxels1_padded, base_name1)
    alg.Cad(voxels2_padded, base_name2)
    
    # Contar el número de voxeles
    num_voxels1 = np.sum(voxels1_padded)
    num_voxels2 = np.sum(voxels2_padded)
    num_voxeles_positivos_1_vs_2 = np.sum(voxeles_positivos_1_vs_2)
    num_voxeles_positivos_2_vs_1 = np.sum(voxeles_positivos_2_vs_1)
    
    print(f"Number of voxels in {base_name1}: {num_voxels1}")
    print(f"Number of voxels in {base_name2}: {num_voxels2}")
    print(f"Number of positive voxels in {base_name2}: {num_voxeles_positivos_2_vs_1}")
    print(f"Number of positive voxels in {base_name1}: {num_voxeles_positivos_1_vs_2}")
