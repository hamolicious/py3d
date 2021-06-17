from py3d.shapes import Prism
import pygame
from time import time
from py3d import Cube
from vector import Color
from math import sin

#region pygame init
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

walk_space = 100
shape = Prism((300, 300 - walk_space, 300), 0, 200, screen)
counter = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	frame_start_time = time()
	screen.fill(0)

	mouse_pos   = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()
	key_press   = pygame.key.get_pressed()

	rot_speed = 70
	shape.rot.x += rot_speed * delta_time
	shape.rot.y += (rot_speed/2) * delta_time
	shape.rot.z += (rot_speed*0.1) * delta_time
	shape.apply_transforms()

	shape.pos.y += (sin(counter) * walk_space) * delta_time
	counter += 1 * delta_time

	shape.display_faces()
	# shape.display_edges()
	# shape.display_verts()

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')




