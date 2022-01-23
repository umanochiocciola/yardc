

# "easter egg"
import pygame.camera
pygame.camera.init()
camlist = pygame.camera.list_cameras()
cam = pygame.camera.Camera(camlist[0], (600, 600))  

cam.start()
img = cam.get_image()
cam.stop()

## ok
