from vectors import *
import pygame
pygame.init()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True
fps = 60
fps_Clock = pygame.time.Clock()
black = (0, 0, 0)
blue = (0, 0, 255)

active_lines = [
    (Segment(Vector((500, 500, 500)), Vector((1000, 500, 500))), black),
    (Segment(Vector((500, 500, 500)), Vector((500, 1000, 500))), black),
    (Segment(Vector((500, 500, 500)), Vector((500, 500, 1000))), black),
    (Segment(Vector((1000, 500, 500)), Vector((1000, 1000, 500))), black),
    (Segment(Vector((1000, 500, 500)), Vector((1000, 500, 1000))), black),
    (Segment(Vector((500, 1000, 500)), Vector((1000, 1000, 500))), black),
    (Segment(Vector((500, 1000, 500)), Vector((500, 1000, 1000))), black),
    (Segment(Vector((500, 500, 1000)), Vector((1000, 500, 1000))), black),
    (Segment(Vector((500, 500, 1000)), Vector((500, 1000, 1000))), black),
    (Segment(Vector((1000, 1000, 500)), Vector((1000, 1000, 1000))), black),
    (Segment(Vector((1000, 500, 1000)), Vector((1000, 1000, 1000))), black),
    (Segment(Vector((500, 1000, 1000)), Vector((1000, 1000, 1000))), black),
]

for i in range(1, 2000, 40):
    active_lines.append((Segment(Vector((i, 0, 0)), Vector((i + 20, 0, 0))), blue))
    active_lines.append((Segment(Vector((0, i, 0)), Vector((0, i + 20, 0))), blue))
    active_lines.append((Segment(Vector((0, 0, i)), Vector((0, 0, i + 20))), blue))


cam = Camera(Vector((-100, 0, -100)), Vector((10, -10, 0)), 150)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        cam.add_position(Vector((10, 0, 0)))
        print(f"Camera position: {cam.position.return_pos()}")
    if keys[pygame.K_s]:
        cam.add_position(Vector((-10, 0, 0)))
        print(f"Camera position: {cam.position.return_pos()}")
    if keys[pygame.K_a]:
        cam.add_position(Vector((0, 10, 0)))
        print(f"Camera position: {cam.position.return_pos()}")
    if keys[pygame.K_d]:
        cam.add_position(Vector((0, -10, 0)))
        print(f"Camera position: {cam.position.return_pos()}")
    if keys[pygame.K_r]:
        cam.add_position(Vector((0, 0, 10)))
        print(f"Camera position: {cam.position.return_pos()}")
    if keys[pygame.K_f]:
        cam.add_position(Vector((0, 0, -10)))
        print(f"Camera position: {cam.position.return_pos()}")
    if keys[pygame.K_z]:
        cam.zoom(1)
        print(f"Zoom is now {cam.fov}")
    if keys[pygame.K_x]:
        cam.zoom(-1)
        print(f"Zoom is now {cam.fov}")



    window.fill((255, 255, 255))
    for line, colour in active_lines:
        start, end = line.project(cam)
        start = [i + 1000 for i in start]
        end = [i + 1000 for i in end]
        pygame.draw.line(window, colour, start, end, 2)


    pygame.display.flip()
    fps_Clock.tick(fps)

pygame.quit()