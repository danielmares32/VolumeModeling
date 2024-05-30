import numpy as np
import os
import trimesh
from scipy.optimize import linear_sum_assignment

def Cad(m1,file):
  vector = np.argwhere(m1.data)  # Obtener las coordenadas no nulas (o algún criterio específico) en m1.data
# Abrir un archivo para escritura
  with open(f"{file}.scr", 'w') as archivo:
      # Iterar a través del vector y escribir las coordenadas exactas
      for dx, dy, dz in vector:
          # Escribir el formato especificado en el archivo con las coordenadas actuales del vector
          archivo.write(f"_box\nC\n{dx},{dy},{dz}\nC\n1\n")


def mesh_to_voxels(mesh, voxel_size=1):
    # Voxelize the mesh
    voxelized = mesh.voxelized(voxel_size)
    # Convert to dense array
    voxels = voxelized.matrix
    return voxels

def pad_voxels(voxels, target_shape):
    padded_voxels = np.zeros(target_shape, dtype=bool)
    original_shape = voxels.shape
    padded_voxels[:original_shape[0], :original_shape[1], :original_shape[2]] = voxels
    return padded_voxels

def calculate_discrete_compactness(voxels):
    # Calcular el área de contacto (Ac)
    contact_area = 0
    total_surface_area = 0
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    # Iterar a través de todos los voxeles
    for x in range(voxels.shape[0]):
        for y in range(voxels.shape[1]):
            for z in range(voxels.shape[2]):
                if voxels[x, y, z]:
                    exposed_faces = 0
                    total_surface_area += 6
                    for direction in directions:
                        nx, ny, nz = x + direction[0], y + direction[1], z + direction[2]
                        if 0 <= nx < voxels.shape[0] and 0 <= ny < voxels.shape[1] and 0 <= nz < voxels.shape[2]:
                            if not voxels[nx, ny, nz]:
                                exposed_faces += 1
                        else:
                            exposed_faces += 1
                    contact_area += exposed_faces

    n = np.sum(voxels)
    Ac_min = n - 1
    Ac_max = 3 * (n - n ** (2 / 3))
    compactness = (contact_area - Ac_min) / (Ac_max - Ac_min)

    return compactness

def find_obj_files(directory):
    obj_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.obj')]
    return obj_files

def calculate_cost_matrix(voxels1, voxels2):
    # Obtener las posiciones de los voxeles activos
    voxels_1 = np.argwhere(voxels1)
    voxels_2 = np.argwhere(voxels2)

    # Crear la matriz de costos basada en la distancia euclidiana con float32
    cost_matrix = np.linalg.norm(voxels_1[:, np.newaxis].astype(np.float32) - voxels_2[np.newaxis, :].astype(np.float32), axis=2)
    
    return cost_matrix

# Función para calcular el trabajo usando el algoritmo húngaro
def calculate_work(voxels1, voxels2, obj_file):
    cost_matrix = calculate_cost_matrix(voxels1, voxels2)

    # Round the cost matrix to 2 decimal places
    cost_matrix_rounded = np.around(cost_matrix, 2)
    # Save the rounded cost matrix to a file with 2 decimal places
    np.savetxt(f'cost_matrix_{obj_file}.txt', cost_matrix_rounded, fmt='%.2f')
    
    # Aplicar el algoritmo húngaro
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # Calcular el trabajo total como la suma de las distancias
    total_work = cost_matrix[row_ind, col_ind].sum()
    return total_work
