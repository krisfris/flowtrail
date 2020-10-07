import numpy as np

from flowtrail.camera import Camera
from flowtrail.fps import Fps
from flowtrail.mesh import TriangleMesh
import config


class Scene:
    def __init__(self):
        self.camera = Camera(position=np.array((0.0, 0.0, 30.0)))
        self.fps = Fps()
        self.nodes = []

    def window_size_changed(self, w, h):
        pass

    def update(self):
        self.fps.update()

    def add_triangles(self, val):
        mesh = TriangleMesh(val)
        mesh.update()
        self.nodes.append(mesh)

    def drop(self):
        pass
