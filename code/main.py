import os
import importlib

if importlib.util.find_spec("cv2") is None:
    os.system('pip install opencv-python')

if importlib.util.find_spec("thymiodirect") is None:
    os.system('pip install thymiodirect')

if importlib.util.find_spec("pygame") is None:
    os.system('pip install pygame')

if importlib.util.find_spec("numpy") is None:
    os.system('pip install numpy')


import cv2
import pygame
import numpy as np
from camera import Camera
from thymio_controller import ThymioController

pygame.init()
pygame.joystick.init()
window_size = (1280, 760)
screen = pygame.display.set_mode(window_size)
font = pygame.font.Font(None, 36)

# TODO create text box in UI to put this url
video_ip = "10.101.120.96"
video_url = "http://%s:4747/video" % (video_ip)
camera = Camera(video_url)
controller = ThymioController()
controller.connect()
pressed_keys = {}

def handle_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controller.disconnect()
            camera.disconnect()
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                controller.disconnect()
                camera.disconnect()
                pygame.quit()
                quit()

            pressed_keys[event.key] = True

        if event.type == pygame.KEYUP:
            pressed_keys.pop(event.key, None)
        

while True:
    screen.fill((255, 255, 255))
    frame, after_frame = camera.run()

    color_surface = pygame.surfarray.make_surface(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    gray_surface = pygame.surfarray.make_surface(cv2.cvtColor(after_frame, cv2.COLOR_BGR2RGB))

    screen.fill((255, 255, 255))
    screen.blit(color_surface, (0, 0))
    screen.blit(gray_surface, (window_size[0] // 2, 0))
    text = font.render("Press Q to quit", True, (0, 0, 0))
    screen.blit(text, (10, window_size[1] - 40))
    pygame.display.update()

    handle_inputs()
    controller.run(pressed_keys)
