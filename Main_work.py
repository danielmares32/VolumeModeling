import trimesh
import numpy as np
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from sklearn.decomposition import PCA
import alg 

def align_mesh_with_pca(mesh):
    points = mesh.vertices - mesh.centroid
    pca = PCA(n_components=3)
    aligned_points = pca.fit_transform(points)
    aligned_mesh = trimesh.Trimesh(vertices=aligned_points, faces=mesh.faces)
    return aligned_mesh

# Función para procesar cada archivo y calcular los resultados
def process_file(obj_file, max_compactness_file, voxels1, results, is_same_file):
    mesh2 = trimesh.load_mesh(obj_file)
    aligned_mesh2 = align_mesh_with_pca(mesh2)  # Alinear la malla
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
    voxeles_positivos = np.logical_and(voxels2_padded, np.logical_not(voxels1_padded))
    
    if is_same_file:
        total_work = 0
        num_voxeles_positivos = 0
    else:
        # Calcular el trabajo usando el algoritmo húngaro
        total_work = alg.calculate_work(voxels1_padded, voxeles_positivos, os.path.basename(obj_file))
        # Contar el número de voxeles
        num_voxeles_positivos = np.sum(voxeles_positivos)
    
    print(f"Number of positive voxels in {obj_file} (not in {max_compactness_file}): {num_voxeles_positivos}")
    print(f"Total work to transform {obj_file} to {max_compactness_file}: {total_work}")
    
    # Añadir resultados a la lista
    results.append({
        'Object Name': os.path.basename(obj_file),
        'Compactness': compactness_values[obj_file],
        'Positive Voxels': num_voxeles_positivos,
        'Total Work': total_work
    })

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
    aligned_mesh = align_mesh_with_pca(mesh)  # Alinear la malla
    voxels = alg.mesh_to_voxels(aligned_mesh)
    compactness = alg.calculate_discrete_compactness(voxels)
    compactness_values[obj_file] = compactness
    if compactness > max_compactness:
        max_compactness = compactness
        max_compactness_file = obj_file

# Imprimir resultados
print("\nResultados de compacidad:")
for obj_file, compactness in compactness_values.items():
    print(f"{obj_file}: {compactness}")

print(f"Archivo con mayor compacidad: {max_compactness_file} con compacidad {max_compactness}")

# Cargar el archivo con la mayor compacidad
mesh1 = trimesh.load_mesh(max_compactness_file)
aligned_mesh1 = align_mesh_with_pca(mesh1)
voxels1 = alg.mesh_to_voxels(aligned_mesh1)

# Lista para almacenar resultados
results = []

# Usar ThreadPoolExecutor para paralelizar el procesamiento de archivos
with ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(process_file, obj_file, max_compactness_file, voxels1, results, obj_file == max_compactness_file)
        for obj_file in obj_files
    ]
    for future in futures:
        future.result()  # Esperar a que cada tarea termine

# Crear un DataFrame de pandas y guardar como archivo Excel
df = pd.DataFrame(results)
df.to_excel('Results.xlsx', index=False)

print("Resultados guardados en 'Results.xlsx'")
