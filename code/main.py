import os
import importlib

# Install the required libraries if they are not in the system yet
if importlib.util.find_spec("cv2") is None:
    os.system('pip install opencv-python')

if importlib.util.find_spec("thymiodirect") is None:
    os.system('pip install thymiodirect')

if importlib.util.find_spec("pygame") is None:
    os.system('pip install pygame')

if importlib.util.find_spec("numpy") is None:
    os.system('pip install numpy')

import pygame
from camera import *
from thymio_controller import *

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
window_size = (1280, 760)
screen = pygame.display.set_mode(window_size)
font = pygame.font.Font(None, 32)
video_ip_text = ""

camera = Camera()
controller = ThymioController()
controller.connect()
pressed_keys = {}


def handle_inputs():
    global video_ip_text
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controller.disconnect()
            camera.disconnect()
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not camera.status in [CONNECTING, CONNECTED]:
                video_ip = video_ip_text.strip()
                camera.connect(video_ip)
            elif event.key == pygame.K_ESCAPE:
                controller.disconnect()
                camera.disconnect()
                pygame.quit()
                quit()
            elif event.key == pygame.K_BACKSPACE:
                video_ip_text = video_ip_text[:-1]
            else:
                if len(video_ip_text) > 20:
                    return
                video_ip_text += event.unicode

            pressed_keys[event.key] = True

        if event.type == pygame.KEYUP:
            pressed_keys.pop(event.key, None)
        
while True:
    handle_inputs()

    screen.fill((255, 255, 255))

    # Show the frame to enter the camera IP address
    if camera.status in [DISCONNECTED, ERROR, CONNECTING]:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(5, 30, 300, 32), 2)
        enter_ip_text = font.render("Enter the camera's IP address then press RETURN", True, (0, 0, 0))
        ip_text = font.render(video_ip_text, True, (0, 0, 0))
        camera_status_text = font.render("Status: " + camera.status, True, (0, 0, 0))
        screen.blit(enter_ip_text, (5, 5))
        screen.blit(ip_text, (10, 35))
        screen.blit(camera_status_text, (5, 70))

    # If the camera is connected, show the next frame
    elif camera.status == CONNECTED:
        screen.fill((255, 255, 255))
        wasd_text = font.render("Use WASD keys to manually control the robot", True, (0, 0, 0))
        quit_text = font.render("Press ESCAPE to quit", True, (0, 0, 0))
        left_motor_text = font.render("Left Motor Speed: " + str(controller.left_motor_speed), True, (0, 0, 0))
        right_motor_text = font.render("Right Motor Speed: " + str(controller.right_motor_speed), True, (0, 0, 0))
        screen.blit(left_motor_text, (10, window_size[1] - 90))
        screen.blit(right_motor_text, (260, window_size[1] - 90))
        screen.blit(wasd_text, (10, window_size[1] - 60))
        screen.blit(quit_text, (10, window_size[1] - 30))

        # Get and show the original and processed frames from the camera
        original_frame, processed_frame = camera.run()
        if original_frame is not None and processed_frame is not None:
            color_surface = pygame.surfarray.make_surface(original_frame)
            gray_surface = pygame.surfarray.make_surface(processed_frame)
            screen.blit(color_surface, (0, 0))
            screen.blit(gray_surface, (window_size[0] // 2, 0))

        controller.run(pressed_keys)

    pygame.display.update()
    clock.tick(30)
