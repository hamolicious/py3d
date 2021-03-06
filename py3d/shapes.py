from vector import Vec3d, Color
from py3d.primitives import Vertex, Face
import pygame

class Shape:
	@staticmethod
	def from_obj_file(filepath, pos: Vec3d, rot: Vec3d, size: Vec3d, screen: pygame.Surface):
		shape = Shape(pos, rot, size, screen)

		with open(filepath, 'r') as file:
			raw_data = file.readlines()

		vertecies = []
		faces = []

		for line in raw_data:
			if line.startswith('v '):
				x, y, z = line.replace('v ', '').split(' ')
				v = Vertex((float(x), float(y), float(z)))
				vertecies.append(v)
			elif line.startswith('f '):
				f = Face([])
				for index in line.replace('f ', '').split(' '):
					f.indecies.append(int(index.split('/')[0])-1)
				faces.append(f)

		shape._DEFAULT_VERTS = vertecies
		shape._DEFAULT_FACES = faces

		return shape

	def get_defualt_verts(self):
		return [i.copy() for i in self._DEFAULT_VERTS]

	def get_defualt_faces(self):
		return [i.copy() for i in self._DEFAULT_FACES]

	def __init__(self, pos: Vec3d, rot: Vec3d, size: Vec3d, screen: pygame.Surface) -> None:
		self._DEFAULT_VERTS = []
		self._DEFAULT_FACES = []

		self.pos = Vec3d(pos)
		self.rot = Vec3d(rot)
		self.size = Vec3d(size)

		self.verts = self.get_defualt_verts()
		self.faces = self.get_defualt_faces()

		self.screen = screen

		self.face_color = Color.random()
		self.edge_color = Color.random()
		self.vert_color = Color.random()

	#region Properties

	@property
	def vertex_count(self):
		return len(self.verts)

	@property
	def face_count(self):
		return len(self.faces)

	#endregion Properties

	def assign_parent(self):
		for f in self.faces:
			f.parent = self

		for v in self.verts:
			v.parent = self

	def apply_transforms(self):
		self.verts = self.get_defualt_verts()
		self.faces = self.get_defualt_faces()
		self.assign_parent()

		for v in self.verts:
			v.pos.mult(self.size)

			v.rotate_x(self.rot.x)
			v.rotate_y(self.rot.y)
			v.rotate_z(self.rot.z)

		# sort faces
		def face_sorter(elem: Face):
			pos = Vec3d.zero()

			for i in elem.indecies:
				pos.add(self.verts[i].pos + self.pos)

			pos.div(len(elem.indecies))
			return pos.dist(Vec3d(300, 300, -300))
		self.faces.sort(key=face_sorter, reverse=True)

	def display_verts(self):
		for v in self.verts:
			v.display(self.screen)

	def display_edges(self):
		for f in self.faces:
			f.display_edge(self.screen)

	def display_faces_unlit(self):
		for f in self.faces:
			f.display_face_unlit(self.screen)

	def display_faces(self):
		for f in self.faces:
			f.display_face(self.screen)


class Cube(Shape):
	def get_defualt_verts(self):
		return [i.copy() for i in self._DEFAULT_VERTS]

	def get_defualt_faces(self):
		return [i.copy() for i in self._DEFAULT_FACES]

	def __init__(self, pos: Vec3d, rot: Vec3d, size: Vec3d, screen: pygame.Surface) -> None:
		super().__init__(pos, rot, size, screen)

		self._DEFAULT_VERTS = [
			Vertex((-0.5, -0.5, -0.5)), # 0
			Vertex(( 0.5, -0.5, -0.5)), # 1
			Vertex(( 0.5, -0.5,  0.5)), # 2
			Vertex((-0.5, -0.5,  0.5)), # 3
			Vertex((-0.5,  0.5, -0.5)), # 4
			Vertex(( 0.5,  0.5, -0.5)), # 5
			Vertex(( 0.5,  0.5,  0.5)), # 6
			Vertex((-0.5,  0.5,  0.5)), # 7
		]
		self._DEFAULT_FACES = [
			Face([0, 1, 2, 3]), # TOP
			Face([4, 5, 6, 7]), # BOTTOM
			Face([0, 1, 5, 4]), # FRONT
			Face([2, 3, 7, 6]), # BACK
			Face([0, 3, 7, 4]), # LEFT
			Face([1, 2, 6, 5]), # RIGHT
		]


class Prism(Shape):
	def get_defualt_verts(self):
		return [i.copy() for i in self._DEFAULT_VERTS]

	def get_defualt_faces(self):
		return [i.copy() for i in self._DEFAULT_FACES]

	def __init__(self, pos: Vec3d, rot: Vec3d, size: Vec3d, screen: pygame.Surface) -> None:
		super().__init__(pos, rot, size, screen)

		self._DEFAULT_VERTS = [
			Vertex((   0,  0.5,    0)), # 0
			Vertex((-0.5, -0.5, -0.5)), # 1
			Vertex(( 0.5, -0.5, -0.5)), # 2
			Vertex(( 0.5, -0.5,  0.5)), # 3
			Vertex((-0.5, -0.5,  0.5)), # 4
		]
		self._DEFAULT_FACES = [
			Face([0, 1, 2]),
			Face([0, 2, 3]),
			Face([0, 3, 4]),
			Face([0, 4, 1]),
			Face([1, 2, 3, 4]),
		]














