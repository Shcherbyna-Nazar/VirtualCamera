import numpy as np


def generate_vertices_file():
    vertices = [
        [-2, -2, 2], [2, -2, 2], [2, 2, 2], [-2, 2, 2],
        [-2, -2, -2], [2, -2, -2], [2, 2, -2], [-2, 2, -2]
    ]
    cube_positions = [[-5, 0, 5], [5, 0, 5], [5, 0, -5], [-5, 0, -5]]

    with open('vertices.txt', 'w') as file:
        for i, pos in enumerate(cube_positions):
            file.write(f'# Cube {i + 1} at position {pos}\n')
            cube_vertices = np.array(vertices) + np.array(pos)
            for vertex in cube_vertices:
                line = ' '.join(map(str, vertex))
                file.write(line + '\n')
            file.write('\n')  # Add a newline for better separation between cubes


generate_vertices_file()
