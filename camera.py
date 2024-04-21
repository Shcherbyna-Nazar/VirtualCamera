import numpy as np


class Camera:
    def __init__(self, position, look_at, up, fov, aspect_ratio, near, far):
        self.position = np.array(position, dtype=np.float32)
        self.forward = np.array(position) - np.array(look_at, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.right = np.cross(self.up, self.forward)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        print("Initialize camera!")
        print(f'Up->{up}')
        print(f'Right->{self.right}')
        print(f'FOr->{up}')

        self.update_matrices()

    def update_matrices(self):
        print(self.fov)
        self.forward = Camera.normalize(self.forward)
        self.right = Camera.normalize(np.cross(self.up, self.forward))
        self.up = Camera.normalize(np.cross(self.forward, self.right))

        self.view_matrix = np.eye(4)
        self.view_matrix[0, :3] = self.right
        self.view_matrix[1, :3] = self.up
        self.view_matrix[2, :3] = -self.forward
        self.view_matrix[:3, 3] = -np.dot(self.view_matrix[:3, :3], self.position)

        f = 1.0 / np.tan(np.radians(self.fov / 2))
        self.projection_matrix = np.array([
            [f / self.aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far + self.near) / (self.near - self.far),
             (2 * self.far * self.near) / (self.near - self.far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)

    def move(self, direction, amount):
        if direction == "forward":
            move_dir = -self.forward
        elif direction == "backward":
            move_dir = self.forward
        elif direction == "right":
            move_dir = -self.right
        elif direction == "left":
            move_dir = self.right
        elif direction == "up":
            move_dir = self.up
        elif direction == "down":
            move_dir = -self.up

        self.position += move_dir * amount
        self.update_matrices()

    def rotate(self, angle, axis):
        rad = np.radians(angle)
        if axis == 'x':
            axis_vec = self.right
        elif axis == 'y':
            axis_vec = self.up
        elif axis == 'z':
            axis_vec = self.forward

        cos_theta, sin_theta = np.cos(rad), np.sin(rad)
        axis_vec = Camera.normalize(axis_vec)
        R = np.array([
            [cos_theta + axis_vec[0] ** 2 * (1 - cos_theta),
             axis_vec[0] * axis_vec[1] * (1 - cos_theta) - axis_vec[2] * sin_theta,
             axis_vec[0] * axis_vec[2] * (1 - cos_theta) + axis_vec[1] * sin_theta],
            [axis_vec[1] * axis_vec[0] * (1 - cos_theta) + axis_vec[2] * sin_theta,
             cos_theta + axis_vec[1] ** 2 * (1 - cos_theta),
             axis_vec[1] * axis_vec[2] * (1 - cos_theta) - axis_vec[0] * sin_theta],
            [axis_vec[2] * axis_vec[0] * (1 - cos_theta) - axis_vec[1] * sin_theta,
             axis_vec[2] * axis_vec[1] * (1 - cos_theta) + axis_vec[0] * sin_theta,
             cos_theta + axis_vec[2] ** 2 * (1 - cos_theta)]
        ])
        self.forward = np.dot(R, self.forward)
        self.up = np.dot(R, self.up)
        self.right = np.cross(self.up, self.forward)
        self.update_matrices()

    def zoom(self, factor):
        # Zoom affects the field of view, reducing it to zoom in, increasing it to zoom out
        self.fov /= (1 + factor * 0.1)  # Adjust zoom factor sensitivity as needed
        self.fov = min(self.fov, 180)
        self.update_matrices()

    @staticmethod
    def normalize(v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    def project(self, vertex):
        camera_coords = np.dot(self.view_matrix, np.append(vertex, 1))
        if camera_coords[2] < 0:
            return None
        projected = np.dot(self.projection_matrix, camera_coords)
        if projected[3] == 0:
            return None
        projected /= projected[3]
        return (projected[0] + 1) * 0.5 * 800, (1 - projected[1]) * 0.5 * 600
