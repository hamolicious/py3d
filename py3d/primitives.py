from vector import Vec3d, Color
from math import sin, cos, radians
import pygame

class Vertex:
	def __init__(self, pos: Vec3d) -> None:
		self.pos = Vec3d(pos)
		self.parent = None

	def copy(self):
		return Vertex(self.pos.copy())

	def rotate_x(self, a):
		a = radians(a)
		self.pos.rotate_x(a)

	def rotate_y(self, a):
		a = radians(a)
		self.pos.rotate_y(a)

	def rotate_z(self, a):
		a = radians(a)
		self.pos.rotate_z(a)

	def to2d(self):
		return (self.pos + self.parent.pos).get_int()[:2]

	def display(self, screen):
		pygame.draw.circle(screen, self.parent.vert_color.get(), self.to2d(), 2)

class Face:
	def __init__(self, indecies: list[int]) -> None:
		self.indecies = indecies
		self.parent = None

	def copy(self):
		return Face(self.indecies.copy())

	def get_normal_vec(self):
		# calculate normal
		a = self.parent.verts[self.indecies[1]].pos - self.parent.verts[self.indecies[0]].pos
		b = self.parent.verts[self.indecies[3]].pos - self.parent.verts[self.indecies[0]].pos

		normal = Vec3d.zero()
		normal.x = (a.y * b.z) - (a.z * b.y)
		normal.y = (a.z * b.x) - (a.x * b.z)
		normal.z = (a.x * b.y) - (a.y * b.x)
		normal.normalise()

		# check if inward or outward
		face_pos = Vec3d.zero()

		for i in self.indecies:
			face_pos.add(self.parent.verts[i].pos)

		face_pos.div(len(self.indecies))
		to_object = face_pos - Vec3d.zero()
		face_pos.normalise()

		p = self.project_vec(face_pos, normal)
		if p > 0 : normal.mult(-1)

		return normal

	def project_vec(self, v1, v2):
		return v1.dot_product(v2) / v1.length

	def display_edge(self, screen):
		p = []
		for i in self.indecies:
			p.append(self.parent.verts[i].to2d())

		proj = self.project_vec(Vec3d(0, 0, 1), self.get_normal_vec())
		if proj > 0:
			pygame.draw.polygon(screen, self.parent.edge_color.get(), p, 2)

	def display_face_unlit(self, screen):
		p = []
		for i in self.indecies:
			p.append(self.parent.verts[i].to2d())

		proj = self.project_vec(Vec3d(0, 0, 1), self.get_normal_vec())
		if proj > 0:
			pygame.draw.polygon(screen, self.parent.face_color.get(), p)

	def display_face(self, screen):
		p = []
		for i in self.indecies:
			p.append(self.parent.verts[i].to2d())

		proj = self.project_vec(Vec3d(0, 0, 1), self.get_normal_vec())

		if proj > 0:
			color = self.parent.face_color.copy()
			color *= (proj + 1) / 2
			pygame.draw.polygon(screen, color.get(), p)









