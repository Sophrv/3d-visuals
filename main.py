from graphics import *
import pygame
pygame.init()

# , pygame.FULLSCREEN
width = 1920
height = 1000
window = pygame.display.set_mode((width, height))
running = True
fps = 60
fps_Clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 30)
showing_stats = False
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)


points = [
    Vector((5, 5, 5)),
    Vector((5, 5, 10)),
    Vector((5, 10, 5)),
    Vector((5, 10, 10)),
    Vector((10, 5, 5)),
    Vector((10, 5, 10)),
    Vector((10, 10, 5)),
    Vector((10, 10, 10)),
    Vector((0, 2, 0)),
    Vector((0, 2, 3)),
    Vector((2, 2, 0)),
    Vector((2, 2, 3)),
    Vector((0, 2, 1.5)),
    Vector((2, 2, 1.5)),
    Vector((3, 2, 0)),
    Vector((3, 2, 2)),
    Vector((3, 2, 2.8)),
    Vector((3, 2, 3)),
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
    (Segment(points[8], points[9]), blue),
    (Segment(points[10], points[11]), blue),
    (Segment(points[12], points[13]), blue),
    (Segment(points[14], points[15]), blue),
    (Segment(points[16], points[17]), blue),
]



active_lines += [(Segment(Vector((i/10, 0, 0)), Vector((i/10+0.6, 0, 0))), red) for i in range(0, 1000, 20)]
active_lines += [(Segment(Vector((0, i/10, 0)), Vector((0, i/10+0.6, 0))), green) for i in range(0, 1000, 20)]
active_lines += [(Segment(Vector((0, 0, i/10)), Vector((0, 0, i/10+0.6))), blue) for i in range(0, 1000, 20)]




cam = Camera(Vector((-10, 5, 5)), 250)

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
    window.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        cam.add_position(Vector((0.10*math.cos(cam.yaw), 0.10*math.sin(cam.yaw), 0)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_s]:
        cam.add_position(Vector((-0.10*math.cos(cam.yaw), -0.10*math.sin(cam.yaw), 0)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_a]:
        cam.add_position(Vector((0.10*math.sin(cam.yaw), -0.10*math.cos(cam.yaw), 0)))
        print(f"Camera position: {cam.position.get_pos()}")
    if keys[pygame.K_d]:
        cam.add_position(Vector((-0.10*math.sin(cam.yaw), 0.10*math.cos(cam.yaw), 0)))
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
    if keys[pygame.K_i]:
        cam.turn_vertical(-math.pi/128)
        print(f"Pitch is now {cam.pitch}")
        print(f"Camera facing vector is now {cam.facing}")
    if keys[pygame.K_j]:
        cam.turn_horizonal(-math.pi/128)
        print(f"Yaw is now {cam.yaw}")
        print(f"Camera facing vector is now {cam.facing}")
    if keys[pygame.K_k]:
        cam.turn_vertical(math.pi/128)
        print(f"Pitch is now {cam.pitch}")
        print(f"Camera facing vector is now {cam.facing}")
    if keys[pygame.K_l]:
        cam.turn_horizonal(math.pi/128)
        print(f"Yaw is now {cam.yaw}")
        print(f"Camera facing vector is now {cam.facing}")
    if keys[pygame.K_p]:
        cam.turn_horizonal(-cam.yaw)
        cam.turn_vertical(-cam.pitch)
        cam.turn_roll(-cam.roll)
        print(f"Looking at +x")
    if keys[pygame.K_c]:
        cam.turn_roll(math.pi/128)
        print(f"Roll is now {cam.roll}")
        print(f"Camera upwards vector is now {cam.upwards}")
    if keys[pygame.K_v]:
        cam.turn_roll(-math.pi/128)
        print(f"Roll is now {cam.roll}")
        print(f"Camera upwards vector is now {cam.upwards}")
    if keys[pygame.K_1]:
        showing_stats = True
    if keys[pygame.K_2]:
        showing_stats = False

    for line, colour in active_lines:
        start, end = line.project(cam)
        start = (start[0] + width / 2, start[1] + height / 2)
        end = (end[0] + width / 2, end[1] + height / 2)
        pygame.draw.line(window, colour, start, end, 2)
    pygame.draw.line(window, blue, (width / 2 - 10, height / 2), (width / 2 + 10, height / 2), 1)
    pygame.draw.line(window, blue, (width / 2, height / 2 - 10), (width / 2, height / 2 + 10), 1)

    if showing_stats:
        for i, info in enumerate([
            font.render(f"FPS: {fps_Clock.get_fps():.2f}", False, blue),
            font.render(f"Position: ({cam.position.x:.2f}, {cam.position.y:.2f}, {cam.position.z:.2f})", False, black),
            font.render(f"Yaw: {cam.yaw:.2f} / {math.degrees(cam.yaw):.1f}", False, black),
            font.render(f"Pitch: {cam.pitch:.2f} / {math.degrees(cam.pitch):.1f}", False, black),
            font.render(f"Roll: {cam.roll:.2f} / {math.degrees(cam.roll):.1f}", False, black),
        ]):
            window.blit(info, (0, i*30))


    pygame.display.flip()
    fps_Clock.tick(fps)

pygame.quit()