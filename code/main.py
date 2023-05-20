import os
import importlib
from importlib import util

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
pygame.display.set_caption('Thymio Robot Shape Finder')
clock = pygame.time.Clock()
window_size = (1280, 760)
screen = pygame.display.set_mode(window_size)
font = pygame.font.Font(None, 32)

background_color = (0, 0, 0)
text_color = (255, 255, 255)
button_size = 100
button_padding = 20
button_coords = [(window_size[0] - 130, window_size[1] - 130), 
                 (window_size[0] - 260, window_size[1] - 130), 
                 (window_size[0] - 390, window_size[1] - 130), 
                 (window_size[0] - 130, window_size[1] - 260), 
                 (window_size[0] - 260, window_size[1] - 260), 
                 (window_size[0] - 390, window_size[1] - 260)]
default_color = (200, 200, 200)
selected_color = (0, 130, 0)
buttons = []
selected_button_index = None
button_colors = [default_color] * len(button_coords)
for coord in button_coords:
    button_rect = pygame.Rect(coord[0], coord[1], button_size, button_size)
    buttons.append(button_rect)
buttons.reverse()

video_ip_text = "192.168.1.73"
camera = Camera()
controller = ThymioController(camera)
controller.connect()
pressed_keys = {}


def handle_inputs():
    global video_ip_text, selected_button_index
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controller.disconnect()
            camera.disconnect()
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and camera.status not in [CONNECTING, CONNECTED]:
                video_ip = video_ip_text.strip()
                camera.connect(video_ip)
            elif event.key == pygame.K_ESCAPE:
                controller.disconnect()
                camera.disconnect()
                pygame.quit()
                quit()
            elif event.key == pygame.K_BACKSPACE and not camera.status == CONNECTING:
                video_ip_text = video_ip_text[:-1]
            elif not camera.status == CONNECTING:
                if len(video_ip_text) > 20:
                    return
                video_ip_text += event.unicode
            pressed_keys[event.key] = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(buttons):
                if button_rect.collidepoint(mouse_pos):
                    button_colors[i] = selected_color
                    if selected_button_index is not None:
                        button_colors[selected_button_index] = default_color
                    selected_button_index = i
                    controller.set_desired_shape(i)

        if event.type == pygame.KEYUP:
            pressed_keys.pop(event.key, None)


while True:
    handle_inputs()

    screen.fill(background_color)

    # Show the frame to enter the camera IP address
    if camera.status in [DISCONNECTED, ERROR, CONNECTING]:
        pygame.draw.rect(screen, text_color, pygame.Rect(5, 30, 300, 32), 2)
        enter_ip_text = font.render("Enter the camera's IP address then press RETURN", True, text_color)
        ip_text = font.render(video_ip_text, True, text_color)
        camera_status_text = font.render(f"Status: {camera.status}", True, text_color)
        screen.blit(enter_ip_text, (5, 5))
        screen.blit(ip_text, (10, 35))
        screen.blit(camera_status_text, (5, 70))

    # If the camera is connected, show the next frame
    elif camera.status in [CONNECTED, DETECTING, DEBUG]:
        screen.fill(background_color)

        # Get and show the original and processed frames from the camera
        original_frame = camera.original_frame
        processed_frame = camera.processed_frame
        if original_frame is not None and processed_frame is not None:
            screen.blit(original_frame, (0, 0))
            screen.blit(processed_frame, (window_size[0] // 2, 0))

        controller.run(pressed_keys)

        for i, button_rect in enumerate(buttons):
            pygame.draw.rect(screen, button_colors[i], button_rect)
            if i == 0:
                pygame.draw.polygon(screen, background_color, [(button_rect.centerx, button_rect.top + 10), (button_rect.left + 10, button_rect.bottom - 10), (button_rect.right - 10, button_rect.bottom - 10)])
            elif i == 1:
                pygame.draw.rect(screen, background_color, button_rect.inflate(-20, -20))
            elif i == 2:
                pygame.draw.polygon(screen, background_color, [(button_rect.centerx, button_rect.top + 10), (button_rect.left + 10, button_rect.centery), (button_rect.left + button_size // 3, button_rect.bottom - 10), (button_rect.right - button_size // 3, button_rect.bottom - 10), (button_rect.right - 10, button_rect.centery)])
            elif i == 3:
                pygame.draw.circle(screen, background_color, button_rect.center, button_size // 2 - 10)

        if controller.is_connected:
            status_text = font.render(f"Current Node: {type(controller.top_node.get_running_node()).__name__}", True, text_color)
            screen.blit(status_text, (10, window_size[1] - 90))
        shapes_text = font.render(f"Detected Shapes: {', '.join(map(str, camera.detected_shapes))}", True, text_color)
        quit_text = font.render("Press ESCAPE to quit", True, text_color)
        screen.blit(shapes_text, (10, window_size[1] - 60))
        screen.blit(quit_text, (10, window_size[1] - 30))

    pygame.display.update()
    clock.tick(30)
