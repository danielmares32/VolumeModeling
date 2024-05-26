import numpy as np
from scipy.optimize import linear_sum_assignment
import time
import trimesh

# Load the .obj files
mesh1 = trimesh.load_mesh('./Objetos/Sphere1_9824.obj')
mesh2 = trimesh.load_mesh('./Objetos/Gato_9824.obj')

# Extract the voxel data
voxels_1 = mesh1.vertices
voxels_2 = mesh2.vertices

# Medir el tiempo de inicio para el cálculo de la matriz de costos
start_time = time.time()

# Crear la matriz de costos basada en la distancia euclidiana
# Get the size of the voxels_2 array
size = min(len(voxels_1), len(voxels_2))
# Create the cost matrix
cost_matrix = np.zeros((size, size))
for i in range(size):
    for j in range(size):
        cost_matrix[i, j] = np.linalg.norm(voxels_1[i] - voxels_2[j])
        
# Round the cost matrix to 2 decimal places
cost_matrix_rounded = np.around(cost_matrix, 2)
# Save the rounded cost matrix to a file with 2 decimal places
np.savetxt('cost_matrix.txt', cost_matrix_rounded, fmt='%.2f')


# Medir el tiempo después de calcular la matriz de costos
cost_matrix_time = time.time()
print(f"Tiempo para calcular la matriz de costos: {cost_matrix_time - start_time} segundos")

# Aplicar el algoritmo húngaro
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Medir el tiempo después de aplicar el algoritmo húngaro
end_time = time.time()
print(f"Tiempo para ejecutar el algoritmo húngaro: {end_time - cost_matrix_time} segundos")
print(f"Tiempo total de ejecución: {end_time - start_time} segundos")

# Open the output file
with open('output.txt', 'w') as f:
    # Write the optimal assignment to the file
    for i in range(len(row_ind)):
        f.write(f"Voxel {row_ind[i]} del primer conjunto asignado al voxel {col_ind[i]} del segundo conjunto\n")
