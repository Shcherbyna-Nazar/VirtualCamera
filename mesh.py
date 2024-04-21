import numpy as np
import pygame


class Mesh:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def draw(self, camera, screen):
        for edge in self.edges:
            start_vertex = self.vertices[edge[0]]
            end_vertex = self.vertices[edge[1]]
            start_projected = camera.project(start_vertex)
            end_projected = camera.project(end_vertex)

            if start_projected is None and end_projected is None:
                continue  # Both vertices are behind the camera
            elif start_projected is not None and end_projected is not None:
                # Invert the y-coordinate to correctly map to Pygame's screen coordinates
                start_projected = (start_projected[0], 600 - start_projected[1])
                end_projected = (end_projected[0], 600 - end_projected[1])
                pygame.draw.line(screen, (255, 255, 255), start_projected, end_projected)
            else:
                # Perform clipping if one vertex is behind the camera and the other is in front
                clipped_vertex = self.clip_line_to_near_plane(start_vertex, end_vertex, camera)
                if clipped_vertex is not None:
                    if start_projected is None:
                        start_projected = camera.project(clipped_vertex)
                    else:
                        end_projected = camera.project(clipped_vertex)
                    if start_projected and end_projected:
                        # Again, invert the y-coordinate post projection
                        start_projected = (start_projected[0], 600 - start_projected[1])
                        end_projected = (end_projected[0], 600 - end_projected[1])
                        pygame.draw.line(screen, (255, 255, 255), start_projected, end_projected)

    def clip_line_to_near_plane(self, start, end, camera):
        # Transform vertices into camera coordinates
        start_cam = np.dot(camera.view_matrix, np.append(start, 1))
        end_cam = np.dot(camera.view_matrix, np.append(end, 1))

        # Check if clipping is needed (one vertex is behind the near plane)
        if (start_cam[2] >= camera.near and end_cam[2] >= camera.near) or (
                start_cam[2] < camera.near and end_cam[2] < camera.near):
            return None  # Both vertices are either completely in front or behind the near plane

        # Calculate interpolation factor (t) for the clipping point
        t = (camera.near - start_cam[2]) / (end_cam[2] - start_cam[2])
        # Interpolate the vertex on the near plane
        clipped_vertex = start + t * (end - start)
        return clipped_vertex


class Pyramid(Mesh):
    def __init__(self, base_center, base_size, height):
        h = height / 2
        s = base_size / 2
        vertices = [
            [base_center[0] - s, base_center[1], base_center[2] - s],  # Base: bottom left
            [base_center[0] + s, base_center[1], base_center[2] - s],  # Base: bottom right
            [base_center[0] + s, base_center[1], base_center[2] + s],  # Base: top right
            [base_center[0] - s, base_center[1], base_center[2] + s],  # Base: top left
            [base_center[0], base_center[1] + height, base_center[2]]  # Apex: above base center
        ]
        edges = [(0, 1), (1, 2), (2, 3), (3, 0),  # Base edges
                 (0, 4), (1, 4), (2, 4), (3, 4)]  # Sides to apex
        super().__init__(np.array(vertices), edges)
