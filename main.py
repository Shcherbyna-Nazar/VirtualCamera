import pygame
import numpy as np
from camera import Camera
from mesh import Mesh, Pyramid


def load_vertices_from_file(filename='vertices.txt'):
    with open(filename, 'r') as file:
        content = file.read()

    blocks = content.strip().split('\n\n')  # Split into blocks
    cubes = []
    for block in blocks:
        lines = block.split('\n')[1:]  # Skip the comment line
        vertices = [list(map(float, line.split())) for line in lines if line.strip()]
        cubes.append(np.array(vertices))
    return cubes


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    camera = Camera(
        position=[0, 0, 20],
        look_at=[0, 0, 0],
        up=[0, 1, 0],
        fov=90,
        aspect_ratio=800 / 600,
        near=0.1,
        far=1000
    )

    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
             (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]

    cubes = [Mesh(vertices, edges) for vertices in load_vertices_from_file()]

    pyramid = Pyramid([0, 10, 0], 5, 6)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera.move("forward", 0.3)
        if keys[pygame.K_s]:
            camera.move("backward", 0.3)
        if keys[pygame.K_a]:
            camera.move("left", 0.3)
        if keys[pygame.K_d]:
            camera.move("right", 0.3)
        if keys[pygame.K_r]:
            camera.move("up", 0.3)
        if keys[pygame.K_f]:
            camera.move("down", 0.3)
        if keys[pygame.K_UP]:
            camera.rotate(1.5, 'x')  # Look up
        if keys[pygame.K_DOWN]:
            camera.rotate(-1.5, 'x')  # Look down
        if keys[pygame.K_LEFT]:
            camera.rotate(-1.5, 'y')  # Look left
        if keys[pygame.K_RIGHT]:
            camera.rotate(1.5, 'y')  # Look right

        if keys[pygame.K_q]:
            camera.rotate(-1.5, 'z')
        if keys[pygame.K_e]:
            camera.rotate(1.5, 'z')
        if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
            camera.zoom(0.1)  # Zoom in
        if keys[pygame.K_MINUS]:
            camera.zoom(-0.1)  # Zoom out

        screen.fill((0, 0, 0))
        for cube in cubes:
            cube.draw(camera, screen)

        pyramid.draw(camera, screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
