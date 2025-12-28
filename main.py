from graphics import *
import pygame
pygame.init()

# , pygame.FULLSCREEN
window = pygame.display.set_mode((1920, 1000))
running = True
fps = 60
fps_Clock = pygame.time.Clock()
black = (0, 0, 0)
blue = (0, 0, 255)


points = [
    Vector((5, 5, 5)),
    Vector((5, 5, 10)),
    Vector((5, 10, 5)),
    Vector((5, 10, 10)),
    Vector((10, 5, 5)),
    Vector((10, 5, 10)),
    Vector((10, 10, 5)),
    Vector((10, 10, 10))
]


active_lines = [
    (Segment(points[0], points[4]), black),
    (Segment(points[0], points[2]), black),
    (Segment(points[0], points[1]), black),
    (Segment(points[4], points[6]), black),
    (Segment(points[4], points[5]), black),
    (Segment(points[2], points[6]), black),
    (Segment(points[2], points[3]), black),
    (Segment(points[1], points[5]), black),
    (Segment(points[1], points[3]), black),
    (Segment(points[6], points[7]), black),
    (Segment(points[5], points[7]), black),
    (Segment(points[3], points[7]), black),
]



cam = Camera(Vector((-100, 0, 0)), 0, 0, 100)

for line, colour in active_lines:
    start, end = line.project(cam)
    start = [i + 500 for i in start]
    end = [i + 500 for i in end]
    print(f"{start} | {end}")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        cam.add_position(Vector((0.10, 0, 0)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_s]:
        cam.add_position(Vector((-0.10, 0, 0)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_a]:
        cam.add_position(Vector((0, 0.10, 0)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_d]:
        cam.add_position(Vector((0, -0.10, 0)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_r]:
        cam.add_position(Vector((0, 0, 0.10)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_f]:
        cam.add_position(Vector((0, 0, -0.10)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_z]:
        cam.zoom(1)
        print(f"Zoom is now {cam.fov}")
    if keys[pygame.K_x]:
        cam.zoom(-1)
        print(f"Zoom is now {cam.fov}")



    window.fill((255, 255, 255))
    for line, colour in active_lines:
        start, end = line.project(cam)
        start = tuple([i + 500 for i in start])
        end = tuple([i + 500 for i in end])
        pygame.draw.line(window, colour, start, end, 2)


    pygame.display.flip()
    fps_Clock.tick(fps)

pygame.quit()